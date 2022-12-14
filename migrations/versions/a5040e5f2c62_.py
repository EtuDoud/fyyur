"""empty message

Revision ID: a5040e5f2c62
Revises: fcb91ff389b5
Create Date: 2022-08-17 17:04:38.543598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5040e5f2c62'
down_revision = 'fcb91ff389b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('genres', sa.String(length=120), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=False),
    sa.Column('facebook_link', sa.String(length=120), nullable=False),
    sa.Column('website_link', sa.String(length=120), nullable=False),
    sa.Column('seeking_description', sa.String(length=500), nullable=False),
    sa.Column('seeking_venue', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('genres', sa.String(length=120), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=False),
    sa.Column('facebook_link', sa.String(length=120), nullable=False),
    sa.Column('website_link', sa.String(length=120), nullable=False),
    sa.Column('seeking_talent', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('venue')
    op.drop_table('artist')
    op.drop_constraint('shows_venue_id_fkey', 'shows', type_='foreignkey')
    op.drop_constraint('shows_artist_id_fkey', 'shows', type_='foreignkey')
    op.create_foreign_key(None, 'shows', 'artists', ['artist_id'], ['id'])
    op.create_foreign_key(None, 'shows', 'venues', ['venue_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.create_foreign_key('shows_artist_id_fkey', 'shows', 'artist', ['artist_id'], ['id'])
    op.create_foreign_key('shows_venue_id_fkey', 'shows', 'venue', ['venue_id'], ['id'])
    op.create_table('artist',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('website_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='artist_pkey')
    )
    op.create_table('venue',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('website_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='venue_pkey')
    )
    op.drop_table('venues')
    op.drop_table('artists')
    # ### end Alembic commands ###
