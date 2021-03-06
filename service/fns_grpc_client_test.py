import sys
import grpc
import os

sys.path.append("./service_spec")
import fake_news_score_pb2 as pb2
import fake_news_score_pb2_grpc as pb2_grpc

GRPC_SERVER = 'localhost:' + os.environ['SERVICE_PORT']

def get_fakenews_score(channel):
    stub = pb2_grpc.FakeNewsScoreStub(channel)
    example = pb2.InputFNS()
    example.headline = 'Melania Trump cancels plans to attend Tuesday rally citing Covid recovery'
    example.body = '''Melania Trump is canceling her first campaign appearance in
    months because she is not feeling well as she continues to recover from
    Covid-19.  She had been set to join President Donald Trump's rally in
    Pennsylvania on Tuesday night, but she has decided not to go. "Mrs. Trump
    continues to feel better every day following her recovery from Covid-19, but
    with a lingering cough, and out of an abundance of caution, she will not be
    traveling today," said Stephanie Grisham, the first lady's chief of staff.
    It would have been the first lady's first in-person appearance at a campaign
    event, outside of August's Republican National Convention speech at the
    White House, in more than a year, when she joined the President last June at
    the official reelection kick-off rally in Florida. Trump wrote an essay last
    week that her symptoms of Covid-19, "hit me all at once and it seemed to be
    a roller coaster." She described having body aches, a cough, headaches and
    feeling extreme fatigue. There are no plans for Melania Trump to make up for
    the rally, according to a source familiar with the first lady's schedule.
    The first lady "did not offer options for another campaign appearance, at a
    rally or otherwise. Let's put it this way, there was no discussion of a rain
    date," the source told CNN. Melania Trump's health issues are "genuine" and
    "she has a persistent cough," they added. "This is not the time to stay
    completely out of the spotlight," the source added. The first lady was not
    expected to give solo remarks at Tuesday's Pennsylvania event. Travel
    restrictions due to coronavirus throughout the last several months, and her
    own bout with Covid-19, hindered Trump's work schedule, Grisham told CNN.
    However, the President, vice president and other members of the Trump family
    have hit the campaign trail. Melania Trump has not historically been a
    visible campaign presence, eschewing appearances while other Trump
    surrogates crisscross the country. In the entire 2016 election cycle, Trump
    gave only a handful of solo speeches. Her longest in Pennsylvania, was just
    five days before the 2016 election, and came after a months' long hiatus
    from the campaign trail. "I'm an immigrant, and let me tell you that nobody
    values the freedom and opportunity of America more than me," said Trump at
    the time, after an introduction by second lady Karen Pence, an active
    campaigner in both 2016 and 2020. In 2016, the most the public saw of their
    future first lady was her presence at the presidential debates, something
    Trump is doing this time around, as well. She attended Trump's debate
    against Democratic rival Joe Biden in Ohio, and she is expected to attend
    the final 2020 presidential debate on Thursday in Nashville, Tennessee. If
    2016 showed a hesitant potential first-spouse, 2020 is proving Trump remains
    ambivalent to the barnstorming ways of her stepchildren, all of whom have
    been hosting campaign events for the last several weeks in key battleground
    states. With few big-name Republican surrogates outside of his family, and
    lack of participation from his wife, Trump's adult children are doing most
    of the talking to voters, with the President himself committing in recent
    days to two to three rallies in a 24-hour period. This week, Ivanka Trump
    will make stops in Michigan, Wisconsin, North Carolina and Florida; Eric
    Trump heads to New Hampshire and Michigan, while his wife, Lara Trump, a
    member of the reelection campaign, goes to Nevada and Arizona; Donald Trump
    Jr. will be at events in North Carolina and Pennsylvania.'''

    try:
        res = stub.fn_score_calc(example)
        print(res)
    except grpc.RpcError as e:
        status_code = e.code()
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            print("Invalid arguments for FakeNews score service call")
        elif grpc.StatusCode.PERMISSION_DENIED == status_code:
            print("Permission denied to FakeNews score service call")
        elif grpc.StatusCode.RESOURCE_EXHAUSTED == status_code:
            print("Call to FakeNews score service denied because of resource exhaustion")
        elif grpc.StatusCode.CANCELLED == status_code:
            print("Call to FakeNews score cancelled by the user")
        elif grpc.StatusCode.UNIMPLEMENTED == status_code:
            print("Method is not implemented or is not supported/enabled in this service.")
        else:
            print("FakeNews score service server is unreachable")

with grpc.insecure_channel(GRPC_SERVER) as channel:
    get_fakenews_score(channel)


