from database import MUNICIPALITIES
from database.models import BiddingExemption
from gazette import locations


class SectionParsing:

    def __init__(self, session):
        self.session = session

    def condition(self):
        return 'is_parsed = FALSE'

    def update(self, gazettes):
        for gazette in gazettes:
            municipality = MUNICIPALITIES.get(gazette.municipality_id)
            if municipality:
                parsing_cls = getattr(locations, municipality)
                parser = parsing_cls(gazette.contents)
                self.update_bidding_exemptions(gazette, parser)
            gazette.is_parsed = True

    def update_bidding_exemptions(self, gazette, parser):
        parsed_exceptions = parser.bidding_exemptions()
        if parsed_exceptions:
            for record in gazette.bidding_exemptions:
                self.session.delete(record)
            for attributes in parsed_exceptions:
                record = BiddingExemption(**attributes)
                gazette.bidding_exemptions.append(record)
