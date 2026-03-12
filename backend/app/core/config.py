from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nexus1 OSINT Platform"
    api_prefix: str = "/api/v1"
    debug: bool = False

    postgres_dsn: str = "sqlite:///./nexus1.db"
    redis_url: str = "redis://redis:6379/0"
    neo4j_uri: str = "bolt://neo4j:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "nexusneo4j"
    elasticsearch_url: str = "http://elasticsearch:9200"
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672//"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
