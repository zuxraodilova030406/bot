import aiosqlite
import logging
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any
from config import DB_NAME
from utils.seed_data import CATEGORIES_DATA, INITIAL_PRODUCTS

logger = logging.getLogger(__name__)


def dict_factory(cursor, row):
    """Convert SQLite row to dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@asynccontextmanager
async def get_connection():
    """Create and yield an aiosqlite connection with row factory."""
    async with aiosqlite.connect(DB_NAME) as conn:
        conn.row_factory = dict_factory
        yield conn


async def init_db():
    """Initialize database tables and seed initial data if empty."""
    async with get_connection() as conn:
        # 1. Users Table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                phone TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Categories Table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                emoji TEXT NOT NULL,
                display_order INTEGER DEFAULT 0
            )
        """)

        # 3. Products Table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_code TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                materials TEXT,
                dimensions TEXT,
                price INTEGER NOT NULL,
                photo TEXT NOT NULL,
                status TEXT DEFAULT 'available',
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_code) REFERENCES categories(code)
            )
        """)

        # 4. Orders Table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                order_type TEXT NOT NULL,
                product_id INTEGER,
                dress_color TEXT,
                dress_photo TEXT,
                wedding_date TEXT,
                customer_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                delivery_type TEXT NOT NULL,
                status TEXT DEFAULT 'yangi',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        await conn.commit()

        # Seed categories if not present
        cursor = await conn.execute("SELECT COUNT(*) as cnt FROM categories")
        row = await cursor.fetchone()
        if row and row["cnt"] == 0:
            logger.info("Kategoriyalar jadvali to'ldirilmoqda...")
            for cat in CATEGORIES_DATA:
                await conn.execute(
                    "INSERT INTO categories (code, name, emoji, display_order) VALUES (?, ?, ?, ?)",
                    (cat["code"], cat["name"], cat["emoji"], cat["display_order"])
                )
            await conn.commit()

        # Seed initial sample products if table is empty
        cursor = await conn.execute("SELECT COUNT(*) as cnt FROM products")
        row = await cursor.fetchone()
        if row and row["cnt"] == 0:
            logger.info("Mahsulotlar namunaviy ma'lumotlar bilan to'ldirilmoqda...")
            for prod in INITIAL_PRODUCTS:
                await conn.execute("""
                    INSERT INTO products 
                    (category_code, name, description, materials, dimensions, price, photo, status, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                """, (
                    prod["category_code"],
                    prod["name"],
                    prod.get("description", ""),
                    prod.get("materials", ""),
                    prod.get("dimensions", ""),
                    prod["price"],
                    prod["photo"],
                    prod.get("status", "available")
                ))
            await conn.commit()

    logger.info("Ma'lumotlar bazasi muvaffaqiyatli ishga tushirildi.")


# ==================== User Operations ====================

async def add_user(user_id: int, username: Optional[str], full_name: str) -> None:
    """Save or update user in database."""
    async with get_connection() as conn:
        await conn.execute("""
            INSERT INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name
        """, (user_id, username or "", full_name))
        await conn.commit()


async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve user details by user_id."""
    async with get_connection() as conn:
        cursor = await conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return await cursor.fetchone()


async def get_all_user_ids() -> List[int]:
    """Get all registered user IDs."""
    async with get_connection() as conn:
        cursor = await conn.execute("SELECT user_id FROM users")
        rows = await cursor.fetchall()
        return [r["user_id"] for r in rows]


async def get_total_users_count() -> int:
    """Count total registered users."""
    async with get_connection() as conn:
        cursor = await conn.execute("SELECT COUNT(*) as cnt FROM users")
        row = await cursor.fetchone()
        return row["cnt"] if row else 0


# ==================== Category Operations ====================

async def get_categories() -> List[Dict[str, Any]]:
    """Retrieve all categories sorted by display order."""
    async with get_connection() as conn:
        cursor = await conn.execute("SELECT * FROM categories ORDER BY display_order ASC")
        return await cursor.fetchall()


async def get_category_by_code(code: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single category by code."""
    async with get_connection() as conn:
        cursor = await conn.execute("SELECT * FROM categories WHERE code = ?", (code,))
        return await cursor.fetchone()


# ==================== Product Operations ====================

async def get_products_by_category(category_code: str, active_only: bool = True) -> List[Dict[str, Any]]:
    """Get all products for a specific category."""
    async with get_connection() as conn:
        if active_only:
            cursor = await conn.execute(
                "SELECT * FROM products WHERE category_code = ? AND is_active = 1 ORDER BY id ASC",
                (category_code,)
            )
        else:
            cursor = await conn.execute(
                "SELECT * FROM products WHERE category_code = ? ORDER BY id ASC",
                (category_code,)
            )
        return await cursor.fetchall()


async def get_product_by_id(product_id: int) -> Optional[Dict[str, Any]]:
    """Get product by id."""
    async with get_connection() as conn:
        cursor = await conn.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return await cursor.fetchone()


async def add_product(
    category_code: str,
    name: str,
    description: str,
    materials: str,
    dimensions: str,
    price: int,
    photo: str,
    status: str = "available"
) -> int:
    """Insert a new product into the catalog."""
    async with get_connection() as conn:
        cursor = await conn.execute("""
            INSERT INTO products 
            (category_code, name, description, materials, dimensions, price, photo, status, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (category_code, name, description, materials, dimensions, price, photo, status))
        await conn.commit()
        return cursor.lastrowid


async def update_product_price(product_id: int, new_price: int) -> bool:
    """Update price of a product."""
    async with get_connection() as conn:
        cursor = await conn.execute(
            "UPDATE products SET price = ? WHERE id = ?",
            (new_price, product_id)
        )
        await conn.commit()
        return cursor.rowcount > 0


async def update_product_status(product_id: int, new_status: str) -> bool:
    """Update status of a product (available / custom_order)."""
    async with get_connection() as conn:
        cursor = await conn.execute(
            "UPDATE products SET status = ? WHERE id = ?",
            (new_status, product_id)
        )
        await conn.commit()
        return cursor.rowcount > 0


async def delete_product(product_id: int) -> bool:
    """Soft-delete a product (set is_active = 0)."""
    async with get_connection() as conn:
        cursor = await conn.execute(
            "UPDATE products SET is_active = 0 WHERE id = ?",
            (product_id,)
        )
        await conn.commit()
        return cursor.rowcount > 0


async def get_total_active_products_count() -> int:
    """Get total count of active products."""
    async with get_connection() as conn:
        cursor = await conn.execute("SELECT COUNT(*) as cnt FROM products WHERE is_active = 1")
        row = await cursor.fetchone()
        return row["cnt"] if row else 0


async def get_all_active_products() -> List[Dict[str, Any]]:
    """Retrieve all active products across all categories."""
    async with get_connection() as conn:
        cursor = await conn.execute("""
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_code = c.code 
            WHERE p.is_active = 1 
            ORDER BY p.id DESC
        """)
        return await cursor.fetchall()


# ==================== Order Operations ====================

async def create_order(
    user_id: int,
    order_type: str,
    product_id: Optional[int],
    dress_color: str,
    dress_photo: Optional[str],
    wedding_date: str,
    customer_name: str,
    phone_number: str,
    delivery_type: str
) -> int:
    """Insert a new order into the database."""
    async with get_connection() as conn:
        cursor = await conn.execute("""
            INSERT INTO orders 
            (user_id, order_type, product_id, dress_color, dress_photo, wedding_date, customer_name, phone_number, delivery_type, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'yangi')
        """, (
            user_id,
            order_type,
            product_id,
            dress_color,
            dress_photo,
            wedding_date,
            customer_name,
            phone_number,
            delivery_type
        ))
        await conn.commit()
        return cursor.lastrowid


async def get_order_by_id(order_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve order details with product info if applicable."""
    async with get_connection() as conn:
        cursor = await conn.execute("""
            SELECT o.*, p.name as product_name, p.price as product_price 
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.id
            WHERE o.id = ?
        """, (order_id,))
        return await cursor.fetchone()


async def update_order_status(order_id: int, status: str) -> bool:
    """Update order status (e.g. 'bog_landim', 'bajarildi', 'bekor_qilindi')."""
    async with get_connection() as conn:
        cursor = await conn.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            (status, order_id)
        )
        await conn.commit()
        return cursor.rowcount > 0


async def get_total_orders_count() -> int:
    """Count total orders in database."""
    async with get_connection() as conn:
        cursor = await conn.execute("SELECT COUNT(*) as cnt FROM orders")
        row = await cursor.fetchone()
        return row["cnt"] if row else 0


async def get_recent_orders(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent orders for admin."""
    async with get_connection() as conn:
        cursor = await conn.execute("""
            SELECT o.*, p.name as product_name 
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.id
            ORDER BY o.id DESC 
            LIMIT ?
        """, (limit,))
        return await cursor.fetchall()
