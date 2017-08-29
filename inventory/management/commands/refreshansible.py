from django.core.management.base import BaseCommand, CommandError

# ansible import
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

from inventory.models import Host, Interface
from django.db.models import Q

from uuid import UUID
results = {}

class ResultCallback(CallbackBase):
    def v2_runner_on_unreachable(self, result):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_ok(self, result, **kwargs):
        global results
        host = result._host
        # ethernet[n].generatedAddress
        # ethernet[n].addressType
        # ethernet[n].generatedAddressOffset
        # uuid.location
        # uuid.bios
        # ethernet[n].present
        d = results.get(host, {})
        if d: 
            d.update(result._result)
        else:
            results[host] = result._result
        #print(json.dumps({host.name: result._result}, indent=4))

class Command(BaseCommand):
    help = "Refresh hosts' info from ansible"

    def add_arguments(self, parser):
        parser.add_argument('hosts', nargs='+', type=str)


    def run_ansible(self, inv=[]):
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])
        # initialize needed objects
        variable_manager = VariableManager()
        loader = DataLoader()
        
        options = Options(
            connection='ssh', 
            module_path='', 
            forks=100, 
            become=False, 
            become_method="sudo", 
            become_user="root", 
            check=False
        )

        # Instantiate our ResultCallback for handling results as they come in
        results_callback = ResultCallback()

        # create inventory and pass to var manager
        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=inv)
        variable_manager.set_inventory(inventory)

        # create play with tasks
        play_source =  dict(
                name = "Inventory Play",
                hosts = 'all',
                gather_facts = 'yes',
                tasks = [
                    dict(action=dict(module='shell', args="/usr/sbin/dmidecode | grep -i 'UUID:' | sed 's/[\t ]*UUID: //gI'"), become=True, register='dmidecode_out'),
                 ]
            )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                      inventory=inventory,
                      variable_manager=variable_manager,
                      loader=loader,
                      options=options,
                      passwords=None,
                      stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
                  )
            result = tqm.run(play)
        except Exception as e:
            pass
        finally:
            if tqm is not None:
                tqm.cleanup()
        return result

    def handle(self, *args, **options):
        inventory = options['hosts']
        rc = self.run_ansible(inventory)
        for name, values in results.items():
            # retrieve shell task stdout 
            facts = values["ansible_facts"]
            local_name = facts.get('ansible_hostname')
            uuid_str = values.get("stdout") # blanck line
            if uuid_str :
                uuid = UUID(uuid_str)
            else :
                uuid = None

            machine_id_str = facts.get("ansible_machine_id")
            if machine_id_str:
                machine_id = UUID(machine_id_str)
            else :
                machine_id = None 
            interfaces = facts.get("ansible_interfaces")
            interfaces_ids = []
            for inter in interfaces:
                net_int = facts.get('ansible_{0}'.format(inter))
                mac_addr = net_int.get("macaddress")
                if mac_addr:
                    net, created = Interface.objects.get_or_create(
                            mac_address = mac_addr,
                            defaults = {'name': inter}
                    )
                    interfaces_ids.append(net.pk)

            hosts_list = Host.objects.filter(
                    Q(uuid = uuid) &
                    Q(machine_id = machine_id) &
                    Q(netinterface__pk__in = interfaces_ids)
            )
            if hosts_list:
                hosts_db = hosts_list[0]
                hosts_db.local_name = local_name
                hosts_db.save()
            else :

                hosts_db = Host.objects.create(
                        name = local_name, 
                        local_name = local_name,
                        uuid = uuid, 
                        machine_id = machine_id
                )

            nets = Interface.objects.filter(pk__in = interfaces_ids)
            for net in nets:
                net.host=hosts_db
                net.save()




        self.stdout.write(self.style.SUCCESS('Success {0}'.format(rc)))
