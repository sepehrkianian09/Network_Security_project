import json

from . import state_proto_types as storageprotos
from .sessionstate import SessionState
from security.util.enhancedJSONEncoder import EnhancedJSONEncoder


class SessionRecord:
    ARCHIVED_STATES_MAX_LENGTH = 40

    def __init__(self, sessionState=None, serialized=None):
        self.previousStates = []
        if sessionState:
            self.sessionState = sessionState
            self.fresh = False
        elif serialized:
            if type(serialized) == bytes:
                serialized = serialized.decode("utf-8")
            data = json.loads(serialized)
            record = storageprotos.RecordStructure(**data)
            self.sessionState = SessionState(record.current_session)
            self.fresh = False
            for previousStructure in record.previous_sessions:
                self.previousStates.append(SessionState(previousStructure))

        else:
            self.fresh = True
            self.sessionState = SessionState()

    def hasSessionState(self, version, aliceBaseKey):
        if self.sessionState.getSessionVersion() == version and aliceBaseKey == self.sessionState.getAliceBaseKey():
            return True

        for state in self.previousStates:
            if state.getSessionVersion() == version and aliceBaseKey == state.getAliceBaseKey():
                return True

        return False

    def getSessionState(self):
        return self.sessionState

    def getPreviousSessionStates(self):
        return self.previousStates

    def isFresh(self):
        return self.fresh

    def archiveCurrentState(self):
        self.promoteState(SessionState())

    def promoteState(self, promotedState):
        self.previousStates.insert(0, self.sessionState)
        self.sessionState = promotedState
        if len(self.previousStates) > self.__class__.ARCHIVED_STATES_MAX_LENGTH:
            self.previousStates.pop()

    def setState(self, sessionState):
        self.sessionState = sessionState

    def serialize(self):
        previousStructures = [previousState.getStructure() for previousState in self.previousStates]
        record = storageprotos.RecordStructure()
        record.current_session = self.sessionState.getStructure().copy()
        record.previous_sessions.extend(previousStructures)

        return json.dumps(record, cls=EnhancedJSONEncoder)
