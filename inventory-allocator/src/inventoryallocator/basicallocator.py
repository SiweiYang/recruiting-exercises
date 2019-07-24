import copy
from typing import List, Dict


class InventoryAllocator:
    def __init__(self, inventories: List[dict]):
        self.inventories = copy.deepcopy(inventories)

    @classmethod
    def normalize_order(cls, order):
        fulfilled_items = []
        for item in order:
            if not order[item]:
                fulfilled_items.append(item)
        for item in fulfilled_items:
            order.pop(item)

    def allocate(self, order: Dict[str, int]):
        self.normalize_order(order)

        if not self.can_fulfill(order):
            # empty list to indicate no allocation possible
            return []

        return self.fulfill(order)

    def can_fulfill(self, order: Dict[str, int]):
        for item in order:
            amount_to_fulfill = order[item]

            # illegal order cannot be fulfilled
            if amount_to_fulfill < 0:
                return False

            for fulfillment_center in self.inventories:
                inventory = fulfillment_center['inventory']
                stock = inventory.get(item, 0)
                # isolate illegal stock level
                amount_to_fulfill -= max(stock, 0)

            if amount_to_fulfill > 0:
                return False

        return True

    def fulfill(self, order: Dict[str, int], inventories: List[dict] = None):
        # start with full inventory by default
        if inventories == None:
            inventories = self.inventories

        # simplify the order by removing fulfilled entries
        self.normalize_order(order)

        # check if order is entirely fulfilled
        if not order:
            return []

        shipment = {}
        fulfillment_center = inventories[0]
        inventory = fulfillment_center['inventory']

        # fulfill maximal amount from the current fulfillment center
        for item in order:
            if inventory.get(item):
                amount = min(order[item], inventory[item])

                # make sure amount will be legal
                amount = max(amount, 0)

                shipment[item] = amount
                order[item] -= amount
                inventory[item] -= amount

        # fulfill the remaining order and combine the shipments
        # if this is a non-trivial shipment
        shipments = self.fulfill(order, inventories[1:])
        if shipment:
            shipments.append({fulfillment_center['name']: shipment})

        return shipments

