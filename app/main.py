# AMIGO SECRETO / SECRET SANTA
# By Joao Soares
# March 24, 2013
#
# This program gets a list of people, phone numbers and what they want.
# Then, it makes a draw and text everyone who their secret friend is.
# Additionaly, it stores this data in binary so that it can be resent
# if necessary.

import csv, copy, random, pickle, datetime
from twilio.rest import TwilioRestClient

account_sid = "AC0d7fbef51ae3db02db38c55182dfbfcc"
auth_token = "3b51b8fb7c050b7d31fec5f75ef2cb29"
client = TwilioRestClient(account_sid, auth_token)

# I chose to use a Person class instead of a database b/c circular
# references are easier this way, so I can add people on the fly
class Person:
    def __init__(self, name, number, gift=None):
        self.name = name
        self.number = number
        if gift is not '':
            self.gift = gift
        else:
            self.gift = None
    # The friend this person gives the present to is called the recipient
    def AddRecipient(self, Person):
        if Person.name is not self.name:
            self.recipient = Person
            return True
        else:
            return False

class List:
    def __init__(self):
        self.participants=[]
    def FileFromName(self, filename, buffer_="rb"):
        return open(filename, buffer_)
    def LoadFromCSV(self, filename):
        if type(filename) is str:
            filename = open(filename, "rb")
        reader = csv.reader(filename)
        headerline = reader.next()
        for row in reader:
            person = Person(name=row[0], number=row[1], gift=row[2])
            self.participants.append(person)
            print "%s added" % person.name
        print self.participants
    def LoadSaved(self, filename):
        self.participants = pickle.load(open(filename,"rb"))
    def SaveList(self, filename=None):
        if filename is None:
            now = datetime.datetime.now()
            filename = now.strftime("%Y-%m-%d-%H-%M-%S") + ".p"
        print filename
        print self.GetParticipants()
        pickle.dump(self.GetParticipants(), open(filename,"wb"))
        print "Saved Successfully"
    def GetParticipants(self):
        return self.participants
            

class Draw:
    def __init__(self, participants):
        self.names = participants
        self.Start()
    # Starts the draw
    def Start(self):
        recipients = copy.copy(self.names)
        random.shuffle(recipients)
        for person in self.names:
            recipient = recipients.pop()
            while person.AddRecipient(recipient) is False:
                print len(recipients)
                if len(recipients) <= 1:
                    self.Start()
                    break
                recipients.append(recipient)
                random.shuffle(recipients)
                recipient = recipients.pop()
    def RemovePerson(self, participant_name):
        for person in self.names:
            # Find the person who is going to be removed
            if participant_name == person.name:
                leaving_person = person
                for giver in self.names:
                    # Find who had drawed the leaving person
                    if leaving_person.name  == giver.recipient.name:
                        giver.recipient == leaving_person.recipient
    def SendSMS(self, person):
        message_body = "E ai, %s! Nosso Amigo de Pascoa vai ser quarta-feira aqui na escola.  Voce tirou %s" % (person.name, person.recipient.name)
        if person.recipient.gift is not None:
            message_body += ", que quer o ovo %s" % (person.recipient.gift)
            message = client.sms.messages.create(to=person.number,
                                                from_="+19496122442",
                                                body = message_body)
    def SendAllSMS(self):
        for person in self.names:
            self.SendSMS(person)

class Test:
    def Draw(self,draw):
        for person in draw.names:
            print "%s tirou %s (%s) que quer um %s" % (person.name,
                    "SEGREDO","SEGREDO","SEGREDO")

    def List(self,list_):
        for person in list_.GetParticipants():
            message = "%s tirou SEGREDO (SEGREDO)" % (person.name)
            if person.recipient.gift is not None:
                message += "que quer SEGREDO"
            print message

if __name__ == '__main__':
    people = List()
    people.LoadFromCSV('info.csv')
    draw = Draw(people.GetParticipants())
    Test().Draw(draw)
