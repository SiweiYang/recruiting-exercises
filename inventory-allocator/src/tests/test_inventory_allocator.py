import pytest

from hypothesis import given
import hypothesis.strategies as st

from inventoryallocator import InventoryAllocator

@pytest.mark.parametrize("order, inventories, expected", [
    ({}, [], []),                                        # null case basic
    ({}, [{'nam': 'fc', 'inventory': {}}], []),          # null case
    ({}, [{'nam': 'fc', 'inventory': {'item': 0}}], []), # null case

    ({'item': 0}, [{'name': 'fc', 'inventory': {'item': 0}}], []),                    # trivial case
    ({'item': 3}, [{'name': 'fc', 'inventory': {'item': 3}}], [{'fc': {'item': 3}}]), # trivial case
    ({'another_item': 0}, [{'name': 'fc', 'inventory': {'item': 0}}], []),            # trivial case

    ({'another_item': 3}, [{'name': 'fc', 'inventory': {'item': 0}}], []),            # unfulfillable case

    (
        {'item': 3, 'another_item': 5},
        [
            {'name': 'fc0', 'inventory': {'item': 1}},
            {'name': 'fc1', 'inventory': {'item': 1}},
            {'name': 'fc2', 'inventory': {'another_item': 1}},
            {'name': 'fc3', 'inventory': {'another_item': 1}},
            {'name': 'fc4', 'inventory': {}},
            {'name': 'fc5', 'inventory': {'item': 5, 'another_item': 5}},
            ],
        [
            {'fc5': {'item': 1, 'another_item': 3}},
            {'fc3': {'another_item': 1}},
            {'fc2': {'another_item': 1}},
            {'fc1': {'item': 1}},
            {'fc0': {'item': 1}},
            ]),                                             # complex case
    ])
def test_allocation(order, inventories, expected):
    allocator = InventoryAllocator(inventories)
    allocations = allocator.allocate(order)
    assert allocations == expected


# a randomized test to reveal potential weak points of the code
# illegal values like negative amount and empty names, duplicate names will be tested
@given(
        st.dictionaries(st.text(), st.integers()),
        st.lists(st.tuples(st.text(), st.dictionaries(st.text(), st.integers()))))
def test_allocation_randomized(order, inventory_list):
    inventories = []
    for name, inventory in inventory_list:
        inventories.append({
            'name': name,
            'inventory': inventory,
            })
    allocator = InventoryAllocator(inventories)
    allocations = allocator.allocate(order)

    # can add verification on allocations to make sure it's a valid allocations

