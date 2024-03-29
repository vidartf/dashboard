from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class NotebookSQL(Base):
    __tablename__ = 'notebooks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    notebook = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)

    @staticmethod
    def from_dict(nb):
        return NotebookSQL(name=nb['name'],
                           notebook=nb['notebook'],
                           created=nb['created'],
                           modified=nb['modified'])

    def to_dict(self):
        return dict(id=self.id,
                    name=self.name,
                    notebook=self.notebook,
                    created=self.created.strftime('%m/%d/%Y %H:%M:%S'),
                    modified=self.modified.strftime('%m/%d/%Y %H:%M:%S'))

    def __repr__(self):
        return "<Notebook(name='{}'>".format(self.name)
