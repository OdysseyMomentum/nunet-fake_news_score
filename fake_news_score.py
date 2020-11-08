import sys
import grpc
import operator
import time
import os
from concurrent import futures

sys.path.append("./service_spec")
import fake_news_score_pb2 as pb2
import fake_news_score_pb2_grpc as pb2_grpc
import uclnlpfnc_pb2
import uclnlpfnc_pb2_grpc
import fnc_stance_detection_pb2
import fnc_stance_detection_pb2_grpc

FNC_GRPC_PORT =f"localhost{os.getenv('NOMAD_PORT_FNC_GRPC_PORT')}" # port localhost where fnc service runs allocated by nomad
UCL_GRPC_PORT =f"localhost{os.getenv('NOMAD_PORT_UCL_GRPC_PORT')}" # port on localhost where unlnlp service runs allocated by nomad

class GRPCfns(pb2_grpc.FakeNewsScoreServicer):
                     
    def fn_score_calc(self, req, ctxt):
        headline = req.headline
        body = req.body
        fnc_res = get_fnc(headline, body)
        ucl_res = get_uclnlp(headline, body)
        fn_score = pb2.Score()
        fn_score.agree = (fnc_res.pred_agree * 0.5) + (ucl_res.agree * 0.5)
        fn_score.disagree = (fnc_res.pred_disagree * 0.5) + (ucl_res.disagree * 0.5)
        fn_score.discuss = (fnc_res.pred_discuss * 0.5) + (ucl_res.discuss * 0.5)
        fn_score.unrelated = (fnc_res.pred_unrelated * 0.5) + (ucl_res.unrelated * 0.5)		
        fn = {"agree": fn_score.agree, 
                "disagree": fn_score.disagree,
                "discuss" : fn_score.discuss,
                "unrelated" : fn_score.unrelated}
        fn_score.stance = max(fn.items(), key=operator.itemgetter(1))[0]
        return fn_score

def get_uclnlp(headline, body):
    channel_ucl = grpc.insecure_channel(UCL_GRPC_ADD)	
    stub_ucl = uclnlpfnc_pb2_grpc.UCLNLPStanceClassificationStub(channel_ucl)
    in_d = uclnlpfnc_pb2.InputData()
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
        return status_code

def get_fnc(headline, body):
    channel_fnc = grpc.insecure_channel(TALOS_GRPC_ADD)	
    stub_fnc = fnc_stance_detection_pb2_grpc.FNCStanceDetectionStub(channel_fnc)
    example = fnc_stance_detection_pb2.Input()
    example.headline = headline
    example.body = body
    try:
        res = stub_fnc.stance_detection(example)
        return res
    except grpc.RpcError as e:
        status_code = e.code()
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            status_code = "Invalid arguments for SOLAT FNS service call"
        elif grpc.StatusCode.PERMISSION_DENIED == status_code:
            status_code = "Permission denied to SOLAT FNS service call"
        elif grpc.StatusCode.RESOURCE_EXHAUSTED == status_code:
            status_code = "Call to SOLAT FNS service denied because of resource exhaustion"
        elif grpc.StatusCode.CANCELLED == status_code:
            status_code = "Call to SOLAT FNS cancelled by the user"
        elif grpc.StatusCode.UNIMPLEMENTED == status_code:
            status_code = "Method is not implemented or is not supported/enabled in this service."
        else:
            status_code = "SOLAT FNS service is unreachable"
        return status_code

#def fnc_grpc():	
if __name__ == "__main__":
    grpc_port = 13220
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

