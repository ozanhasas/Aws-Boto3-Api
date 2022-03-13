from flask import Flask, request, jsonify, make_response
import boto3
from config import config
import logging

logging.basicConfig(filename=config['log_file'], level=config['log_level'])
app = Flask(__name__)
host = config['host']
port = config['port']


@app.route('/ec2', methods=['GET'])
def api_main():
    return "EC2 API'YE HOŞGELDİNİZ!"


@app.route('/ec2/list', methods=['GET', 'POST'])
def list_instances():
    if request.method == "POST":
        return make_response("Hata Kodu : 405 \n İstek atılırken yanlış metot kullanılmıştır.", 405)
    if request.get_json() is None:
        s_id = request.args.get('aws_access_key_id')
        s_key = request.args.get('aws_secret_access_key')
        region = request.args.get('region_name')
    else:
        temp = request.get_json()
        s_id = temp['aws_access_key_id']
        s_key = temp['aws_secret_access_key']
        region = temp['region_name']
    try:
        client = boto3.client('ec2', aws_access_key_id=s_id, aws_secret_access_key=s_key, region_name=region)
        response = client.describe_instances()
    except Exception as e:
        logging.error(e)
        return make_response(jsonify(Success=False, Error=str(e), Hata="Internal Server Error"), 500)
    instances_list = []
    for i in response['Reservations']:
        instances_list.append(i["Instances"][0]['InstanceId'])
    return make_response(jsonify(Sucsess=True, Instances_list=instances_list), 200)


@app.route("/ec2/start", methods=['GET', 'POST'])
def start_instances():
    if request.method == "GET":
        return make_response(f"Hata Kodu : 405 \n İstek atılırken yanlış metot kullanılmıştır.", 405)
    if request.get_json() is None:
        s_id = request.args.get('aws_access_key_id')
        s_key = request.args.get('aws_secret_access_key')
        region = request.args.get('region_name')
        instances_id = request.args.get('instances_id')
    else:
        temp = request.get_json()
        s_id = temp['aws_access_key_id']
        s_key = temp['aws_secret_access_key']
        region = temp['region_name']
        instances_id = temp['instances_id']
    try:
        client = boto3.client('ec2', aws_access_key_id=s_id, aws_secret_access_key=s_key, region_name=region)
        response = client.start_instances(InstanceIds=[instances_id])
    except Exception as e:
        logging.error(e)
        return make_response(jsonify(Success=False, Instance_id=instances_id, Error=str(e), Hata="Internal Server Error"), 500)
    prev_state = response["StartingInstances"][0]["PreviousState"]["Name"]
    curr_state = response["StartingInstances"][0]["CurrentState"]["Name"]
    return make_response(jsonify(Sucsess=True, Instance_id=instances_id, Previous_State=prev_state, Current_State=curr_state), 200)


@app.route("/ec2/stop", methods=['GET', 'POST'])
def stop_instances():
    if request.method == "GET":
        return make_response("Hata Kodu : 405 \n İstek atılırken yanlış metot kullanılmıştır.", 405)
    if request.get_json() is None:
        s_id = request.args.get('aws_access_key_id')
        s_key = request.args.get('aws_secret_access_key')
        region = request.args.get('region_name')
        instances_id = request.args.get('instances_id')
    else:
        temp = request.get_json()
        s_id = temp['aws_access_key_id']
        s_key = temp['aws_secret_access_key']
        region = temp['region_name']
        instances_id = temp['instances_id']
    try:
        client = boto3.client('ec2', aws_access_key_id=s_id, aws_secret_access_key=s_key, region_name=region)
        response = client.stop_instances(InstanceIds=[instances_id])
    except Exception as e:
        logging.error(e)
        return make_response(jsonify(Success=False, Instance_id=instances_id, Error=str(e), Hata="Internal Server Error"), 500)
    prev_state = response["StoppingInstances"][0]["PreviousState"]["Name"]
    curr_state = response["StoppingInstances"][0]["CurrentState"]["Name"]
    return make_response(jsonify(Sucsess=True, Instance_id=instances_id, Previous_State=prev_state, Current_State=curr_state), 200)


if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)



#pip3 freeze > requirements.txt ||||||| Pythondaki uygulama için gerekli olan paketleri içeren txt dosyası oluşturma.
