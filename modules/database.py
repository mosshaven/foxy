from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional
from pyrogram import enums
import os
import json
import random
from functools import wraps
import time

COOLDOWNS = {}

def cooldown(seconds):
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message):
            user_id = message.from_user.id
            current_time = time.time()
            
            if user_id in COOLDOWNS and current_time - COOLDOWNS[user_id] < seconds:
                remaining = int(seconds - (current_time - COOLDOWNS[user_id]))
                await message.reply_text(
                    f"⏳ | Слишком быстро! Попробуй снова через <code>{remaining}</code> секунд",
                    parse_mode=enums.ParseMode.HTML
                )
                return
            
            COOLDOWNS[user_id] = current_time
            return await func(client, message)
        return wrapper
    return decorator

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    foxy_bucks = Column(Integer, default=0)
    pizzas = Column(Integer, default=0)
    cubes = Column(Integer, default=0)
    angry_kids = Column(Integer, default=0)
    is_banned = Column(Boolean, default=False)
    last_pizza = Column(DateTime, default=None)
    last_case = Column(DateTime, default=None)
    last_command = Column(DateTime, default=None)
    last_pizzeria = Column(DateTime, default=None)

class Database:
    def __init__(self):
        self.engine = create_async_engine(f'sqlite+aiosqlite:///{os.path.abspath("data/fox.db")}')
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
    
    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def get_user(self, user_id):
        async with self.async_session() as session:
            result = await session.get(User, user_id)
            if not result:
                return None
            return result
    
    async def create_user(self, user_id, username, first_name, last_name):
        async with self.async_session() as session:
            user = User(
                id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            session.add(user)
            await session.commit()
            return user
    
    async def update_currency(self, user_id, foxy_bucks=None, pizzas=None, cubes=None):
        async with self.async_session() as session:
            user = await session.get(User, user_id)
            if not user:
                return False
            
            if foxy_bucks is not None:
                user.foxy_bucks = foxy_bucks
            if pizzas is not None:
                user.pizzas = pizzas
            if cubes is not None:
                user.cubes = cubes
            
            await session.commit()
            return True
    
    async def add_currency(self, user_id, foxy_bucks=0, pizzas=0, cubes=0, angry_kids=0):
        async with self.async_session() as session:
            user = await session.get(User, user_id)
            if not user:
                return False
            
            user.foxy_bucks += foxy_bucks
            user.pizzas += pizzas
            user.cubes += cubes
            user.angry_kids += angry_kids
            
            await session.commit()
            return True
    
    async def can_eat_pizza(self, user_id) -> bool:
        user = await self.get_user(user_id)
        if not user:
            return False
            
        if not user.last_pizza or \
           (datetime.now() - user.last_pizza) > timedelta(minutes=15):
            return True
        return False
    
    async def eat_pizza(self, user_id) -> bool:
        if not await self.can_eat_pizza(user_id):
            return False
            
        async with self.async_session() as session:
            user = await session.get(User, user_id)
            user.pizzas += 1
            user.last_pizza = datetime.now()
            await session.commit()
            return True
    
    async def can_open_case(self, user_id) -> bool:
        user = await self.get_user(user_id)
        if not user:
            return False
            
        if not user.last_case or \
           (datetime.now() - user.last_case) > timedelta(hours=24):
            return True
        return False
    
    async def open_case(self, user_id) -> Optional[int]:
        """Returns FB amount won"""
        if not await self.can_open_case(user_id):
            return None
            
        fb_won = random.randint(5, 50)  # Small FB reward
        async with self.async_session() as session:
            user = await session.get(User, user_id)
            user.foxy_bucks += fb_won
            user.last_case = datetime.now()
            await session.commit()
            return fb_won
    
    async def get_top_pizza(self, limit=25) -> list:
        async with self.async_session() as session:
            result = await session.execute(
                select(User).where(User.pizzas > 0).order_by(User.pizzas.desc()).limit(limit)
            )
            return result.scalars().all()
    
    async def save_top_pizza(self):
        top = await self.get_top_pizza()
        data = [
            {
                'id': user.id,
                'username': user.username,
                'pizzas': user.pizzas
            } for user in top
        ]
        with open('data/top.json', 'w') as f:
            json.dump(data, f)
    
    async def can_claim_pizzeria(self, user_id) -> bool:
        user = await self.get_user(user_id)
        if not user or user.pizzas < 1000:
            return False
        
        if not user.last_pizzeria or \
           (datetime.now() - user.last_pizzeria) > timedelta(hours=24):
            return True
        return False
    
    async def claim_pizzeria(self, user_id) -> Optional[int]:
        """Returns FB amount earned from pizzeria"""
        user = await self.get_user(user_id)
        if not user or not await self.can_claim_pizzeria(user_id):
            return None
        
        income = int(user.pizzas / 100)  # pizzas / 100 = FB per day
        async with self.async_session() as session:
            user = await session.get(User, user_id)
            user.foxy_bucks += income
            user.last_pizzeria = datetime.now()
            await session.commit()
            return income

# Initialize database when imported
db = Database()
