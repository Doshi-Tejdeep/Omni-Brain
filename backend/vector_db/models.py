"""
Document metadata model.

This file defines the structure of the document information
that will later be stored in the database.
"""


class Document:
    """
    Represents metadata for an uploaded document.
    """

    def __init__(
    self,
    id,
    filename,
    upload_time=None,
    status="uploaded",
    page_count=0,
    ):
        self.id = id
        self.filename = filename
        self.upload_time = upload_time
        self.status = status
        self.page_count = page_count