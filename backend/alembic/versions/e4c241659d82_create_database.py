"""create database

Revision ID: e4c241659d82
Revises: 
Create Date: 2023-08-22 23:52:03.558372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.scraper.constants import TAGS, COMPANIES

# revision identifiers, used by Alembic.
revision: str = 'e4c241659d82'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    init_sql = '''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                email VARCHAR UNIQUE NOT NULL,
                password_hash VARCHAR NOT NULL,
                is_admin BOOLEAN DEFAULT false
            );

            CREATE TABLE IF NOT EXISTS companies (
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR UNIQUE NOT NULL,
                company_website VARCHAR UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS company_requests (
                request_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                company_name VARCHAR NOT NULL,
                company_website VARCHAR NOT NULL
            );

            CREATE TABLE IF NOT EXISTS jobs (
                job_id SERIAL PRIMARY KEY,
                title VARCHAR NOT NULL,
                company VARCHAR NOT NULL,
                url VARCHAR UNIQUE NOT NULL,
                skills TEXT[] CHECK (CARDINALITY(skills) > 0),
                timestamp TIMESTAMPTZ DEFAULT TIMEZONE('Asia/Tbilisi'::text, NOW())
            );

            CREATE TABLE IF NOT EXISTS tags (
                tag_id SERIAL PRIMARY KEY,
                name VARCHAR UNIQUE NOT NULL,
                value VARCHAR NOT NULL
            );
    '''

    # Insert Tags
    insert_tags_sql = 'INSERT INTO tags(tag_id, name, value) VALUES '

    for k, v in TAGS.items():
        pk = v[0]
        tag_name = k
        tag_value = v[1]

        insert_tags_sql += f'({pk}, \'{tag_name}\', \'{tag_value}\'), '
    
    insert_tags_sql = insert_tags_sql[:-2] + ';'

    # Insert Companies
    insert_companies_sql = 'INSERT INTO companies(company_id, company_name, company_website) VALUES '

    for k, v in COMPANIES.items():

        pk = v[0]
        name = k
        website = v[1]

        insert_companies_sql += f'({pk}, \'{name}\', \'{website}\'), '
    
    insert_companies_sql = insert_companies_sql[:-2] + ';'
    
    op.execute(sa.DDL(init_sql))
    op.execute(insert_tags_sql)
    op.execute(insert_companies_sql)
    pass


def downgrade() -> None:
    op.drop_table('company_requests')
    op.drop_table('tags')
    op.drop_table('jobs')
    op.drop_table('companies')
    op.drop_table('users')
    pass
