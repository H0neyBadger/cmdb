from django.db import models
from organization.models import Team

class Geo(models.Model):
    #TODO gps
    #TODO datacenter rack loction 
    pass

class Asset(models.Model):
    name = models.CharField(max_length=255)
    snow_id = models.CharField(max_length=255, help_text='ServiceNow database ID')
    # one location/asset 
    geo = models.ForeignKey(Geo, on_delete=models.CASCADE, null=True)
    # TODO owner/resp 
    team = models.ForeignKey(Team, related_name="asset", help_text="Assest's team owner", null=True)

    def __str__(self):
        return '%s %s' % (self.name, self.pk)

class Domain(models.Model):
    # partially qualified domain name
    name = models.CharField(max_length=255, help_text='partially qualified domain name', unique=True)
    # reverse arpa

class HardwareType(models.Model):
    # vmware docker phy virt ...
    name = models.CharField(max_length=30, unique=True)

class OSFamily(models.Model):
    # ansible os_family
    name = models.CharField(max_length=30, unique=True)

class OSDistribution(models.Model):
    name = models.CharField(max_length=30, unique=True)
    os_family = models.ForeignKey(OSFamily, on_delete=models.CASCADE)

class OSDistributionMajorVersion(models.Model):
    name = models.CharField(max_length=30, unique=True)
    version =  models.IntegerField()
    os_distribution = models.ForeignKey(OSDistribution, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (("os_distribution", "version"),)

class OSDistributionVersion(models.Model):
    version = models.CharField(max_length=5)
    os_distribution = models.ForeignKey(OSDistribution, on_delete=models.CASCADE)
    os_distribution_major_version = models.ForeignKey(OSDistributionMajorVersion, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ("os_distribution", "version"),
            ("os_distribution_major_version", "version")
        )

class Host(Asset):
    uuid = models.UUIDField(null=True)
    machine_id = models.UUIDField(null=True)
    local_name = models.CharField(max_length=30)
    dns_name = models.CharField(max_length=255)
    vm_name = models.CharField(max_length=30, null=True)
    domain = models.ForeignKey(Domain, null=True)
    hardware_type = models.ForeignKey(HardwareType, null=True)
    parent_host = models.ForeignKey("self", help_text='VM parent host', related_name="guest", null=True)
    # TODO public_keys
    os_family = models.ForeignKey(OSFamily, null=True)
    os_distribution = models.ForeignKey(OSDistribution, null=True)
    os_distribution_version = models.ForeignKey(OSDistributionVersion, null=True) 
    system_team = models.ForeignKey(Team, related_name="system", null=True)
    application_team = models.ForeignKey(Team, related_name="application", null=True)
    # TODO env (dev prod)
    # TODO status (in use, shuted down, decomm...)
    # TODO critical 
    # TODO backup class
    # TODO storage class
    # TODO cpu ram

# todo network class (vlan ip gw netmask ... dmz)

class Interface(models.Model):
    name = models.CharField(max_length=30)
    # TODO mac 64
    mac_address = models.CharField(max_length=18)
    host = models.ForeignKey(Host, related_name="interfaces", on_delete=models.CASCADE, null=True)

class IPAddress(models.Model):
    # TODO ping
    ip = models.GenericIPAddressField()
    # interface = null means dns entry only
    interface = models.ForeignKey(Interface, related_name="ip_address", on_delete=models.CASCADE, null=True)

class DomainName(models.Model):
    # TODO dns record
    name = models.CharField(max_length=30)
    ip_address = models.ForeignKey(IPAddress, related_name="domain_names")

## applis

