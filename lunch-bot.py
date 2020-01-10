class LunchBotHandler(object):
    '''
    Let's get lunch!
    '''

    def usage(self):
        return '''
        lunch-bot is a bot that helps Recursers organize groups to get lunch! Type help to get started.
        '''

    def handle_message(self, message, bot_handler):
        # add your code here

        # bot_handler.send_message(dict(
        #     type='stream', # can be 'stream' or 'private'
        #     to=stream_name, # either the stream name or user's email
        #     subject=subject, # message subject
        #     content=message, # content of the sent message
        # ))

        # bot_handler.storage.put("foo", "bar")  # set entry "foo" to "bar"
        # print(bot_handler.storage.get("foo"))  # print "bar"
        # bot_handler.storage.contains("foo")

        # By default, bot_handler.storage accepts any object for keys and values,
        # as long as it is JSON-able. Internally, the object then gets converted 
        # to a UTF-8 string.

        # Given message is an object
        if message['content'] == "reset":
            bot_handler.send_reply(message, "This will wipe all current lunches from my records. If you wish to continue, please type \"reset confirm\".") 
        if message['content'] == "reset confirm":
            bot_handler.storage.put("lunches", [])

        message_args = message['content'].split()

        if len(message_args) == 0:
            bot_handler.send_reply(message, "Oops! You need to provide a lunch-bot command! Type help for a list of commands I understand :-)")
            return 

        if not self.is_valid_command(message_args[0]):
            bot_handler.send_reply(message, "Oops! {} is not a valid lunch-bot command! Type help for a list of commands I understand :-)".format(message_args[0])) 

        if message_args[0] == "help":
            bot_handler.send_reply(message,'''
            lunch-bot Help
            
            Available Commands:
            help - Displays all available commands that lunch-bot understands

            make-plan [restaurant] [time] - Creates a lunch plan for a given place and time. [restaurant] and [time] must not contain any spaces

            show-plans - Shows all active lunch plans along with their associated lunch_id

            rsvp [lunch_id] - RSVPs to a certain lunch plan, given its [lunch_id] (to see every lunch_id, use the show-plans command)

            my-plans - Shows all lunch plans you have currently RSVP'd to

            un-rsvp [lunch_id] - Removes your RSVP from a certain lunch plan, given its [lunch_id] (to see every lunch_id, use the show-plans command)

            delete-plan [lunch_id] - Deletes a certain lunch plan, given its [lunch_id] (to see every lunch_id, use the show-plans command)
            ''') 

        if message_args[0] == "make-plan":
            # less than two arguments (doesnt have message_args[1] or message_args[2])
            if len(message_args) < 3:
                bot_handler.send_reply(message, "Oops! The make-plan command requires more information. Type help for formatting instructions.")
                return

            plan = {
                "restaurant": message_args[1],
                "time": message_args[2],
                "rsvps": [message['display_recipient']],
            }

            if not (bot_handler.storage.contains("lunches")):
                bot_handler.storage.put("lunches", [plan])
            else:
                lunch_list = bot_handler.storage.get("lunches")
                lunch_list.append(plan)
                bot_handler.storage.put("lunches", lunch_list)
            bot_handler.send_reply(message, "I have added your plan! Enjoy lunch, " + message['display_recipient'] + "!") 

        if message_args[0] == "show-plans":
            if (not (bot_handler.storage.contains("lunches")) or len(bot_handler.storage.get("lunches")) == 0):
                bot_handler.send_reply(message, "There are no lunch plans to show! Why not add one using the make-plan command?")
            else:
                reply = ""
                lunches = bot_handler.storage.get("lunches")
                for i, lunch in enumerate(lunches):
                    reply += (str(i) + ": " + lunch['restaurant'] + " @ " + lunch['time'] + ", " + str(len(lunch['rsvps'])) + " RSVP(s)\n")
                
                reply = reply.rstrip()
                bot_handler.send_reply(message, reply)

        if message_args[0] == "my-plans":
            if (not (bot_handler.storage.contains("lunches")) or len(bot_handler.storage.get("lunches")) == 0):
                bot_handler.send_reply(message, "There are no active lunch plans right now! Why not add one using the make-plan command?")
            else:
                current_user = message['display_recipient']

                reply = "Here are the lunches you've RSVP'd to:\n"
                lunch_list = bot_handler.storage.get("lunches")
                for i, lunch in enumerate(lunch_list):
                    if current_user in lunch['rsvps']:
                        reply += (str(i) + ": " + lunch['restaurant'] + " @ " + lunch['time'] + ", " + str(len(lunch['rsvps'])) + " RSVP(s)\n")
                
                reply = reply.rstrip()
                bot_handler.send_reply(message, reply)


        if message_args[0] == "rsvp":
            # less than one arguments (doesnt have message_args[1])
            if len(message_args) < 2:
                bot_handler.send_reply(message, "Oops! The rsvp command requires more information. Type help for formatting instructions.")
                return

            if (not (bot_handler.storage.contains("lunches")) or len(bot_handler.storage.get("lunches")) == 0):
                bot_handler.send_reply(message, "There are no lunch plans to RSVP to! Why not add one using the make-plan command?")
            else:
                try: 
                    int(message_args[1])
                except ValueError:
                    bot_handler.send_reply(message, "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.")
                    return
                
                rsvp_id = int(message_args[1])
                lunch_list = bot_handler.storage.get("lunches")

                if rsvp_id >= len(lunch_list) or rsvp_id < 0:
                    bot_handler.send_reply(message, "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.")
                    return

                selected_lunch = lunch_list[rsvp_id]

                if message['display_recipient'] in selected_lunch['rsvps']:
                    bot_handler.send_reply(message, "You've already RSVP'd to this lunch_id! Type my-plans to show all of your current lunch plans.")
                    return

                selected_lunch['rsvps'].append(message['display_recipient'])

                lunch_list[rsvp_id] = selected_lunch
                bot_handler.storage.put("lunches", lunch_list)

                bot_handler.send_reply(message, "Thanks for RSVPing to lunch at " + selected_lunch['restaurant'] + "! Enjoy your food, " + message['display_recipient'] + "!")

        if message_args[0] == "un-rsvp" or message_args[0] == "flake":
            # less than one arguments (doesnt have message_args[1])
            if len(message_args) < 2:
                bot_handler.send_reply(message, "Oops! The un-rsvp command requires more information. Type help for formatting instructions.")
                return

            if (not (bot_handler.storage.contains("lunches")) or len(bot_handler.storage.get("lunches")) == 0):
                bot_handler.send_reply(message, "There are no lunch plans to remove your RSVP from! Why not add one using the make-plan command?")
            else:
                try: 
                    int(message_args[1])
                except ValueError:
                    bot_handler.send_reply(message, "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.")
                    return
                
                rsvp_id = int(message_args[1])
                lunch_list = bot_handler.storage.get("lunches")

                if rsvp_id >= len(lunch_list) or rsvp_id < 0:
                    bot_handler.send_reply(message, "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.")
                    return

                selected_lunch = lunch_list[rsvp_id]

                if not message['display_recipient'] in selected_lunch['rsvps']:
                    bot_handler.send_reply(message, "Oops! It looks like you haven't RSVP'd to this lunch_id!")
                    return

                selected_lunch['rsvps'].remove(message['display_recipient'])

                lunch_list[rsvp_id] = selected_lunch
                bot_handler.storage.put("lunches", lunch_list)

                bot_handler.send_reply(message, "You've successfully un-RSVP'd to lunch at " + selected_lunch['restaurant'] + ".")                    

        if message_args[0] == "delete-plan":
            # less than one arguments (doesnt have message_args[1])
            if len(message_args) < 2:
                bot_handler.send_reply(message, "Oops! The delete-plan command requires more information. Type help for formatting instructions.")
                return
            
            if (not (bot_handler.storage.contains("lunches")) or len(bot_handler.storage.get("lunches")) == 0):
                bot_handler.send_reply(message, "There are no lunch plans to delete! Why not add one using the make-plan command?")
            else:
                try: 
                    int(message_args[1])
                except ValueError:
                    bot_handler.send_reply(message, "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.")
                    return

                delete_id = int(message_args[1])
                lunch_list = bot_handler.storage.get("lunches")

                if delete_id >= len(lunch_list) or delete_id < 0:
                    bot_handler.send_reply(message, "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.")
                    return

                del lunch_list[delete_id]
                bot_handler.storage.put("lunches", lunch_list)

                bot_handler.send_reply(message, "You've successfully deleted lunch {}.".format(delete_id)) # See the updated list using the show-plans command!".format(delete_id))
                for i, lunch in enumerate(lunch_list):
                    print(str(i) + ": " + lunch['restaurant'] + " @ " + lunch['time'] + ", " + str(len(lunch['rsvps'])) + " RSVP(s)")

        # bot_handler.send_message(dict(
        #     type='stream',
        #     to='lunch',
        #     subject='yum',
        #     content='hello'
        # ))

    def is_valid_command(self, command):
        commands = ["help", "make-plan", "show-plans", "delete-plan", "rsvp", "un-rsvp", "flake", "my-plans"]
        return command in commands
    

handler_class = LunchBotHandler