from sqlalchemy import Table, Column, Integer, String, MetaData

metadata_chat = MetaData()

chat = Table(
    "chat",
    metadata_chat,
    Column("message", String),
    Column("id", String)  
)

metadata_lists = MetaData()

lists = Table(
    "lists",
    metadata_lists,
    Column("nick", String),
    Column("title", String),
    Column("description", String),
)

metadata_logins = MetaData()

logins = Table(
    "logins",
    metadata_logins,
    Column("nick", String, primary_key=True),
    Column("password", String),
    Column("role", String),
    Column("email", String),
    Column("city", String),
    Column("age", String),
    Column("about", String),
)
