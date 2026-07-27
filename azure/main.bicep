@description('Nombre de la máquina virtual')
param vmName string = 'tdp-server'

@description('Usuario administrador')
param adminUsername string = 'tdp'

@description('Contraseña del usuario')
@secure()
param adminPassword string

@description('Ubicación')
param location string = resourceGroup().location

var setupScript = loadTextContent('vm-setup.sh')

var indentedScript = replace(setupScript, '\n', '\n    ')

var cloudInit = loadTextContent('cloud-init.yaml')

resource nsg 'Microsoft.Network/networkSecurityGroups@2024-05-01' = {
  name: '${vmName}-nsg'
  location: location

  properties: {
    securityRules: [
      {
        name: 'Allow-SSH'

        properties: {
          priority: 1000
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '22'
        }
      }
      {
        name: 'Allow-HTTP'

        properties: {
          priority: 1010
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '80'
        }
      }
    ]
  }
}

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: '${vmName}-vnet'
  location: location

  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }

    subnets: [
      {
        name: 'default'

        properties: {
          addressPrefix: '10.0.0.0/24'
        }
      }
    ]
  }
}

resource nic 'Microsoft.Network/networkInterfaces@2024-05-01' = {
  name: '${vmName}-nic'
  location: location

  properties: {
    networkSecurityGroup: {
      id: nsg.id
    }

    ipConfigurations: [
      {
        name: 'ipconfig'

        properties: {
          subnet: {
            id: vnet.properties.subnets[0].id
          }

          privateIPAllocationMethod: 'Dynamic'
        }
      }
    ]
  }
}

resource vm 'Microsoft.Compute/virtualMachines@2024-03-01' = {
  name: vmName
  location: location

  properties: {

    hardwareProfile: {
      vmSize: 'Standard_B2ats_v2'
    }

    storageProfile: {

      imageReference: {
        publisher: 'debian'
        offer: 'debian-12'
        sku: '12-gen2'
        version: 'latest'
      }

      osDisk: {
        createOption: 'FromImage'
        deleteOption: 'Delete'

        managedDisk: {
          storageAccountType: 'Standard_LRS'
        }
      }
    }

    osProfile: {
      computerName: vmName
      adminUsername: adminUsername
      adminPassword: adminPassword
      customData: base64(cloudInit)

      linuxConfiguration: {
        disablePasswordAuthentication: false
      }
    }

    networkProfile: {
      networkInterfaces: [
        {
          id: nic.id
        }
      ]
    }
  }
}