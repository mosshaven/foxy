from datetime import datetime, timedelta
from modules.database import db, User

COOLDOWN_SECONDS = 3  # Global cooldown for commands

async def check_cooldown(user_id):
    """Check if user can use a command (global cooldown)"""
    user = await db.get_user(user_id)
    if not user:
        return True
    
    if not user.last_command:
        return True
    
    time_passed = (datetime.now() - user.last_command).total_seconds()
    return time_passed >= COOLDOWN_SECONDS

async def get_cooldown_remaining(user_id):
    """Get remaining cooldown time in seconds"""
    user = await db.get_user(user_id)
    if not user or not user.last_command:
        return 0
    
    time_passed = (datetime.now() - user.last_command).total_seconds()
    remaining = max(0, COOLDOWN_SECONDS - time_passed)
    return int(remaining)

async def update_cooldown(user_id):
    """Update user's last command time"""
    async with db.async_session() as session:
        user = await session.get(User, user_id)
        if user:
            user.last_command = datetime.now()
            await session.commit()
