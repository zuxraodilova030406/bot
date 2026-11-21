from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    """FSM states for ordering and custom bridal consultation."""
    # Step 1: Dress color or reference photo
    dress_info = State()
    
    # Step 2: Wedding / Event date
    wedding_date = State()
    
    # Step 3: Customer full name
    customer_name = State()
    
    # Step 4: Phone number
    phone_number = State()
    
    # Step 5: Delivery option
    delivery_type = State()
    
    # Final confirmation
    confirm = State()
