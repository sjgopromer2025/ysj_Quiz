"""submission table create

Revision ID: 8731b61877cd
Revises: 709a85876226
Create Date: 2025-03-30 03:45:41.136105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8731b61877cd'
down_revision: Union[str, None] = '709a85876226'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_quiz_submission_answers_id', table_name='quiz_submission_answers')
    op.drop_table('quiz_submission_answers')
    op.drop_index('ix_quiz_submissions_id', table_name='quiz_submissions')
    op.drop_table('quiz_submissions')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz_submissions',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('quiz_submissions_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quiz_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('score', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('submitted_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], name='quiz_submissions_quiz_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='quiz_submissions_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_quiz_submissions_id', 'quiz_submissions', ['id'], unique=False)
    op.create_table('quiz_submission_answers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('submission_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('question_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('selected_option_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name='quiz_submission_answers_question_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['selected_option_id'], ['option.id'], name='quiz_submission_answers_selected_option_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['submission_id'], ['quiz_submissions.id'], name='quiz_submission_answers_submission_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='quiz_submission_answers_pkey')
    )
    op.create_index('ix_quiz_submission_answers_id', 'quiz_submission_answers', ['id'], unique=False)
    # ### end Alembic commands ###
