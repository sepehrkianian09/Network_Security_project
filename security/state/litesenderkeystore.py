from security.groups.state.senderkeystore import SenderKeyStore
from security.groups.state.senderkeyrecord import SenderKeyRecord
import sqlite3
import sys


class LiteSenderKeyStore(SenderKeyStore):
    def __init__(self, dbConn):
        self.dbConn = dbConn
        dbConn.execute("CREATE TABLE IF NOT EXISTS sender_keys (_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "group_id TEXT NOT NULL,"
                       "sender_id INTEGER NOT NULL, record BLOB);")

        dbConn.execute("CREATE UNIQUE INDEX IF NOT EXISTS sender_keys_idx ON sender_keys (group_id, sender_id);")

    def storeSenderKey(self, senderKeyName, senderKeyRecord):
        q = "INSERT OR REPLACE INTO sender_keys (group_id, sender_id, record) VALUES(?,?, ?)"
        cursor = self.dbConn.cursor()
        serialized = senderKeyRecord.serialize()
        if sys.version_info < (2, 7):
            serialized = memoryview(serialized)
        try:
            cursor.execute(q, (senderKeyName.getGroupId(), senderKeyName.getSender().getName(), serialized))
            self.dbConn.commit()
        except sqlite3.IntegrityError as e:
            q = "UPDATE sender_keys set record = ? WHERE group_id = ? and sender_id = ?"
            cursor = self.dbConn.cursor()
            cursor.execute(q, (serialized, senderKeyName.getGroupId(), senderKeyName.getSender().getName()))
            self.dbConn.commit()

    def loadSenderKey(self, senderKeyName):
        q = "SELECT record FROM sender_keys WHERE group_id = ? and sender_id = ?"
        cursor = self.dbConn.cursor()
        cursor.execute(q, (senderKeyName.getGroupId(), senderKeyName.getSender().getName()))

        result = cursor.fetchone()
        if not result:
            return SenderKeyRecord()
        return SenderKeyRecord(serialized = result[0])
