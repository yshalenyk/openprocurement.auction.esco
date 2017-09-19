from openprocurement.auction.core import Planning, RunDispatcher
from openprocurement.auction.esco.interfaces import IEscoAuction
from openprocurement.auction.esco.constants import PROCUREMENT_METHOD_TYPE
from openprocurement.auction.esco.views import includeme as _includeme

from openprocurement.auction.interfaces import IFeedItem, IAuctionDatabridge,\
    IAuctionsChronograph, IAuctionsServer


def includeme(components):
    components.add_auction(
        IEscoAuction,
        procurementMethodType=PROCUREMENT_METHOD_TYPE
    )
    components.registerAdapter(
        Planning,
        (IAuctionDatabridge, IFeedItem),
        IEscoAuction
    )
    components.registerAdapter(
        RunDispatcher,
        (IAuctionsChronograph, IFeedItem),
        IEscoAuction
    )
    server = components.queryUtility(IAuctionsServer)
    _includeme(server)
