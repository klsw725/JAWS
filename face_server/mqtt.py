import paho.mqtt.client as mqtt


mqttc = mqtt.Client()      # MQTT Client 오브젝트 생성
mqttc.connect("127.0.0.1", 1883)    # MQTT 서버에 연결
while True:
    mqttc.publish("helloworld", "Hello World!")  # 'hello/world' 토픽에 "Hello World!"라는 메시지 발행
    mqttc.loop(2)        # timeout = 2초