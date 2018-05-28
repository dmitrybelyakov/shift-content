# todo: how do we handle field deletions?

# todo: how to address gdpr?
# todo: https://www.michielrook.nl/2017/11/forget-me-please-event-sourcing-gdpr
# todo: https://www.michielrook.nl/2017/11/event-sourcing-gdpr-follow-up/
# todo: 1. we can and must edit events in store
# todo: 2. events must be associated with a user
# todo: 3. all such events will be obfuscated (possibly removed)

# todo: do we actually delete data from the database?
# todo: or simply don't show it?
# todo: if we do, what happens to events in store that have the fields?