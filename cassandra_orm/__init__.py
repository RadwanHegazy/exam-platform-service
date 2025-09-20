import cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
import uuid
from typing import List, Dict, Any, Type, TypeVar, Optional
T = TypeVar('T', bound='BaseModel')

class CassandraORM:
    """Custom ORM for Cassandra database operations"""
    
    _session = None
    _cluster = None
    
    @classmethod
    def connect(cls, hosts: List[str] = ['cassandra-node2', 'cassandra-node1'], port: int = 9042, 
                keyspace: str = 'exam_platform', username: str = None, password: str = None):
        """Establish connection to Cassandra cluster"""
        try:
            if username and password:
                auth_provider = PlainTextAuthProvider(username=username, password=password)
                cls._cluster = Cluster(hosts, port=port, auth_provider=auth_provider)
            else:
                cls._cluster = Cluster(hosts, port=port)
                
            cls._session = cls._cluster.connect()
            cls._create_keyspace(keyspace)
            cls._session.set_keyspace(keyspace)
            cls._session.row_factory = dict_factory
            print("Connected to Cassandra cluster successfully!")
        except Exception as e:
            print(f"Error connecting to Cassandra: {e}")
            raise
    
    @classmethod
    def _create_keyspace(cls, keyspace: str):
        """Create keyspace if it doesn't exist"""
        create_keyspace_query = f"""
        CREATE KEYSPACE IF NOT EXISTS {keyspace}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 3}}
        """
        cls._session.execute(create_keyspace_query)
    
    @classmethod
    def close(cls):
        """Close the connection to Cassandra"""
        if cls._cluster:
            cls._cluster.shutdown()
        print("Connection to Cassandra closed.")

class BaseModel:
    """Base model class that all data models will inherit from"""
    
    class Meta:
        ...

    @classmethod
    def get_table_name(cls) -> str:
        """Get the table name for the model (defaults to class name lowercase)"""
        return cls.__name__.lower()
    
    @classmethod
    def create_table(cls):
        """Create table for the model if it doesn't exist"""
        if not CassandraORM._session:
            raise Exception("Not connected to Cassandra. Call CassandraORM.connect() first.")
        
        # Get field definitions from class attributes
        fields = []
        for attr_name, attr_value in cls.__dict__.items():
            if not attr_name.startswith('_') and attr_name not in ['id', 'get_table_name', 'create_table', 'create', 'get_all', "Meta"]:
                fields.append(f"{attr_name} {attr_value}")
        
        # Create table query
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {cls.get_table_name()} (
            id UUID PRIMARY KEY,
            {', '.join(fields)}
        )
        """
        
        assert hasattr(cls.Meta, 'index'), "Please set Meta.index"
        
        index_name = cls.Meta.index
        create_index_query = f"""
            CREATE INDEX IF NOT EXISTS {index_name} ON {cls.get_table_name()} ({index_name});
        """
            
        
        try:
            CassandraORM._session.execute(create_table_query)
            CassandraORM._session.execute(create_index_query)
            print(f"Table '{cls.get_table_name()}' created successfully!")
        except Exception as e:
            print(f"Error creating table: {e}")
            raise
            
    

    @classmethod
    def create(cls, **kwargs) -> uuid.UUID:
        """Create a new record in the database"""
        if not CassandraORM._session:
            raise Exception("Not connected to Cassandra. Call CassandraORM.connect() first.")
        
        # Generate UUID if not provided
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
        
        # Prepare columns and values
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = list(kwargs.values())
        
        # Insert query
        insert_query = f"""
        INSERT INTO {cls.get_table_name()} ({columns})
        VALUES ({placeholders})
        """
        
        try:
            prepared = CassandraORM._session.prepare(insert_query)
            CassandraORM._session.execute(prepared, values)
            print(f"Record created in '{cls.get_table_name()}' with ID: {kwargs['id']}")
            return kwargs['id']
        except Exception as e:
            print(f"Error creating record: {e}")
            raise

    @classmethod
    def get_by_key(cls, key: str, value: Any) -> List[Dict[str, Any]]:
        """
        Get rows by custom key-value pair.
        NOTE: The key must be indexed (part of primary key or have a secondary index).
        """
        if not CassandraORM._session:
            raise Exception("Not connected to Cassandra. Call CassandraORM.connect() first.")
        query = f"SELECT * FROM {cls.get_table_name()} WHERE {key} = ?"
        try:
            prepared = CassandraORM._session.prepare(query)
            rows = CassandraORM._session.execute(prepared, [value])
            return list(rows)
        except Exception as e:
            print(f"Error fetching rows by {key}: {e}")
            raise