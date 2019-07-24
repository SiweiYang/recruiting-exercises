import yaml
import click

from inventoryallocator.basicallocator import InventoryAllocator


@click.command()
@click.argument('order', type=str)
@click.argument('inventories', type=str)
def allocate(order, inventories):
    '''
    A utility program that optimizes order dispatching from multiple locations.

    It expects

      order: an order in the form of a dictionary where the key is the item and the value is the desired amount

      inventories: a list of locations with their stock level, in the form of a list of structs

    Examples

      \b
      inventory-allocator '{ apple: 10 }' '[{ name: owd, inventory: { apple: 5 } }, { name: dm, inventory: { apple: 5 }}]'

    '''
    order = yaml.load(order, Loader=yaml.SafeLoader)
    inventories = yaml.load(inventories, Loader=yaml.SafeLoader)

    allocator = InventoryAllocator(inventories)
    print(yaml.dump(allocator.allocate(order), default_flow_style=True))

if __name__ == '__main__':
    allocate()
