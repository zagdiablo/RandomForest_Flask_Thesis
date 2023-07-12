import requests
import re


krl = {
    0: ["Pondok Ranji", "-6.3051604,106.6772934"],
    1: ["Sudimara", "-6.3051604,106.6772934"],
    2: ["Jurang Mangu", "-6.3051604,106.6772934"],
    3: ["Rawa Buntu", "-6.314725,106.6006389"],
    4: ["Serpong", "-6.314725,106.6006389"],
    5: ["Cisauk", "-6.3244818,106.5653708"],
    6: ["Stasiun Sukarasa", "-6.1767973,106.5565589"],
}

bus_stop = {
    0: ["McDonald Bintaro Sektor 9", "-6.2803460800438975, 106.71326539274271"],
    1: ["Jl.Bintaro Utama 9 Barat", "-6.278938371116093, 106.71858689525493"],
    2: ["Jl.Bintaro Utama 9 Timur", "-6.279109002703985, 106.71871564128342"],
    3: ["Masjid Jami Al-Falah", "-6.278042554362421, 106.70442483211762"],
    4: ["RM Sederhana", "-6.278341160118203, 106.71828648785502"],
    5: ["Seberang RM Sederhana", "-6.278511791901764, 106.71832940319787"],
    6: ["Seberang Masjid Jami Al Falah", "-6.277914580414691, 106.7042960860891"],
    7: ["Club House Graha Taman", "-6.275611043978805, 106.70674226063099"],
    8: ["Seberang Sekolah Auliya", "-6.2813272082578315, 106.70283696443254"],
    9: ["Sekolah Auliya", "-6.28128455054785, 106.70296571046106"],
}

bandara = {
    0: ["Bandara Pondok Cabe", "-6.334617082667807, 106.76345847477444"],
    1: [
        "Bandara Internasional Soekarno-Hatta",
        "-6.123904836586304, 106.65344269066034",
    ],
}


def get_jarak_googleapi(tempat, tujuan_dict):
    all_jarak = []

    for index in range(len(tujuan_dict)):
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={tempat}&destinations={tujuan_dict[index][1]}&key=AIzaSyAwqGQ5BbN_hu-bSFX7aHvqMDW2C2tK5Yo"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        try:
            distance_data = dict(response.json())["rows"][0]["elements"][0]["distance"][
                "text"
            ]
        except KeyError:
            distance_data = "0.0km"

        try:
            all_jarak.append(
                [
                    tujuan_dict[index][0],
                    float(re.findall(r"\d+\.\d+", distance_data)[0]),
                ]
            )
        except IndexError:
            all_jarak.append([tujuan_dict[index][0], float(0.0)])

    terdekat = None

    jarak_counter = 1000.0
    for nama_tempat, jarak in all_jarak:
        if jarak < jarak_counter:
            jarak_counter = jarak
            terdekat = [nama_tempat, jarak]

    print(terdekat)
    return terdekat


def hitung_jarak_kendaraan_umum(kordinat_rumah):
    hasil_bandara = get_jarak_googleapi(kordinat_rumah, bandara)
    print("bandara done")
    hasil_krl = get_jarak_googleapi(kordinat_rumah, krl)
    print("krl done")
    hasil_bus_stop = get_jarak_googleapi(kordinat_rumah, bus_stop)
    print("bus stop done")

    return {"bandara": hasil_bandara, "krl": hasil_krl, "bus_stop": hasil_bus_stop}
