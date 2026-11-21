from aiogram.fsm.state import State, StatesGroup


class AddProductState(StatesGroup):
    """FSM states for admin adding a new bridal product."""
    category = State()
    name = State()
    materials = State()
    dimensions = State()
    price = State()
    photo = State()
    status = State()


class EditPriceState(StatesGroup):
    """FSM states for editing a product price."""
    product_id = State()
    new_price = State()


class BroadcastState(StatesGroup):
    """FSM states for broadcasting a message to all bot users."""
    message = State()
