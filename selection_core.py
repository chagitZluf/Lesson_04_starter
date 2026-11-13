
"""Selection rules for one event (lesson 4).

The event is a plain dict, as loaded from data/events.json.
Requirements: REQ-SEL-01 .. REQ-SEL-06.
"""

KNOWN_SERVICES = ("add_to_album", "print_10x15")


class SelectionError(Exception):
    """A selection was rejected. `code` says which rule rejected it."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def available_services(event):
    """Known services that are enabled for this event, in catalog order."""
    enabled = event.get("enabled_services", [])
    return [code for code in KNOWN_SERVICES if code in enabled]


def _media_ids_of(event):
    """All media ids in all galleries of the event."""
    ids = set()
    for gallery in event.get("galleries", []):
        ids.update(gallery.get("media", []))
    return ids


def submit_selection(event, actor_id, media_ids, service_codes):
    """Validate a client's selection and record it on the event."""

    # REQ-SEL-06: Only the event's client may submit a selection.
    if actor_id != event.get("client_id"):
        raise SelectionError("FORBIDDEN")

    # REQ-SEL-01: At least one media item is required.
    if not isinstance(media_ids, list) or len(media_ids) == 0:
        raise SelectionError("SELECTION_EMPTY")

    # REQ-SEL-02: Every media item must belong to this event.
    event_media_ids = _media_ids_of(event)
    for media_id in media_ids:
        if media_id not in event_media_ids:
            raise SelectionError("MEDIA_NOT_IN_EVENT")

    # REQ-SEL-03: Every requested service must be known and enabled.
    enabled = available_services(event)
    for code in service_codes:
        if code not in enabled:
            raise SelectionError("SERVICE_NOT_AVAILABLE")

    # REQ-SEL-05: Duplicate media items are not allowed.
    if len(media_ids) != len(set(media_ids)):
        raise SelectionError("DUPLICATE_MEDIA")

    # Only after all checks do we modify the event.
    selections = event.setdefault("selections", [])

    selection = {
        "id": "sel_{:03d}".format(len(selections) + 1),
        "event_id": event["id"],
        "client_id": actor_id,
        "media_ids": list(media_ids),
        "service_codes": list(service_codes),
    }

    selections.append(selection)
    return selection
