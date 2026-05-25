import urllib.request
url_siren = "https://www.soundjay.com/buttons/beep-01a.wav" # Placeholder, buscando el .wav de sirena real
# Este es el link para la sirena de alerta máxima:
url_alert = "https://actions.google.com/sounds/v1/alarms/emergency_it_is_an_emergency.ogg" # OGG no sirve, buscando WAV...
# Usa este (Alerta de Sistema Crítico ):
url_final = "https://www.soundjay.com/misc/sounds/bell-ringing-01.wav" # Distorsionado suena increíble
urllib.request.urlretrieve("https://github.com/rafael-m-silva/simple-python-soundboard/raw/master/sounds/alarm.wav", "access_granted.wav" )
print("🚨 ALERTA NUCLEAR CONFIGURADA")
