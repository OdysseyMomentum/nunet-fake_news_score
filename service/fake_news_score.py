import sys
import grpc
import operator
import time
import os
from concurrent import futures

sys.path.append("./service_spec")
sys.path.append("./service/service_spec")
import fake_news_score_pb2 as pb2
import fake_news_score_pb2_grpc as pb2_grpc

import athenefnc_pb2 
import athenefnc_pb2_grpc
import uclnlp_service_pb2
import uclnlp_service_pb2_grpc
from resutils import *


ATHENE_GRPC_ADD = os.environ['ATHENE_GRPC_ADD'] # port ATHENE service runs
UCL_GRPC_ADD = os.environ['UCL_GRPC_ADD'] # port unlnlp service runs

class GRPCfns(pb2_grpc.FakeNewsScoreServicer):
                     
    def fn_score_calc(self, req, ctxt):
        try:
            telemetry=resutils()
            start_time=time.time()
            cpu_start_time=telemetry.cpu_ticks()
        except:
            pass       
        headline = req.headline
        body = req.body
        ucl_res = get_uclnlp(headline, body)
        athene_res = get_athene(headline, body)
        fn_score = pb2.Score()
        fn_score.agree = (athene_res.agree * 0.5) + (ucl_res.agree * 0.5)
        fn_score.disagree = (athene_res.disagree * 0.5) + (ucl_res.disagree * 0.5)
        fn_score.discuss = (athene_res.discuss * 0.5) + (ucl_res.discuss * 0.5)
        fn_score.unrelated = (athene_res.unrelated * 0.5) + (ucl_res.unrelated * 0.5)		
        fn = {"agree": fn_score.agree, 
                "disagree": fn_score.disagree,
                "discuss" : fn_score.discuss,
                "unrelated" : fn_score.unrelated}
        fn_score.stance = max(fn.items(), key=operator.itemgetter(1))[0]
        try:
            memory_used=telemetry.memory_usage()
            time_taken=time.time()-start_time
            cpu_used=telemetry.cpu_ticks()-cpu_start_time
            net_used=telemetry.block_in()
            telemetry.call_telemetry(str(cpu_used),str(memory_used),str(net_used),str(time_taken))
        except:
            pass	
        return fn_score

def get_uclnlp(headline, body): 
    channel_ucl = grpc.insecure_channel(UCL_GRPC_ADD)	
    stub_ucl = uclnlp_service_pb2_grpc.UCLNLPStanceClassificationStub(channel_ucl)
    in_d = uclnlp_service_pb2.InputData()
    in_d.headline = headline
    in_d.body = body
    try:
        res = stub_ucl.stance_classify(in_d)
        return res
    except grpc.RpcError as e:
        status_code = e.code()
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            status_code = "Invalid arguments for UCLMR FNS service call"
        elif grpc.StatusCode.PERMISSION_DENIED == status_code:
            status_code = "Permission denied to UCLMR FNS service call"
        elif grpc.StatusCode.RESOURCE_EXHAUSTED == status_code:
            status_code = "Call to UCLMR FNS service denied because of resource exhaustion"
        elif grpc.StatusCode.CANCELLED == status_code:
            status_code = "Call to UCLMR FNS cancelled by the user"
        elif grpc.StatusCode.UNIMPLEMENTED == status_code:
            status_code = "Method is not implemented or is not supported/enabled in this service."
        else:
            status_code = "UCLMR FNS service server is unreachable"
        print(status_code)
        return status_code

def get_athene(headline, body):
    channel_athene = grpc.insecure_channel(ATHENE_GRPC_ADD)
    stub_athene = athenefnc_pb2_grpc.AtheneStanceClassificationStub(channel_athene)
    athene = athenefnc_pb2.InputData()
    athene.headline = headline
    athene.body = body
    try:
        res = stub_athene.stance_classify(athene)
        return res
    except grpc.RpcError as e:
        status_code = e.code()
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            status_code = "Invalid arguments for Athene FNS service call"
        elif grpc.StatusCode.PERMISSION_DENIED == status_code:
            status_code = "Permission denied to Athene FNS service call"
        elif grpc.StatusCode.RESOURCE_EXHAUSTED == status_code:
            status_code = "Call to Athene FNS service denied because of resource exhaustion"
        elif grpc.StatusCode.CANCELLED == status_code:
            status_code = "Call to Athene FNS cancelled by the user"
        elif grpc.StatusCode.UNIMPLEMENTED == status_code:
            status_code = "Method is not implemented or is not supported/enabled in this service."
        else:
            status_code = "Athene FNS service is unreachable"
        print(status_code)
        return status_code

#def fnc_grpc():	
if __name__ == "__main__":
    grpc_port = 7009
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_FakeNewsScoreServicer_to_server(GRPCfns(), grpc_server)
    grpc_server.add_insecure_port('[::]:' + str(grpc_port))
    grpc_server.start()
    print("GRPC Server Started on port: " + str(grpc_port))
		
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Exiting....")
        grpc_server.stop(0)

