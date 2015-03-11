#!/usr/bin/env python

__author__ = 'heru'

import hashlib
import random
import base64
import hmac
import datetime

import requests

class BpjsBriding(object):
    BASE_URL = "http://x.x.c/webservices" # disesuaikan dengan URL yang diberikan oleh BPJS

    def __init__(self, customer_id, secret_key):
        self.customer_id = customer_id
        self.secret_key = secret_key
        self.unix_start_time = datetime.datetime(1970, 1, 1)

    def __generate_timestamp(self):
        """
        timestamp digenerate dari hasil pengurangan
        awal penanggalan Sistem Operasi Unix 1-1-1970 dengan
        waktu sekarang (UTC time)
        :return:
        """
        now = datetime.datetime.utcnow()
        timestamp = (now-self.unix_start_time).total_seconds()
        return int(timestamp)

    def __generate_hmac(self, data):
        signature = hmac.new(
            self.secret_key,
            msg=data,
            digestmod=hashlib.sha256
        ).digest()
        encoded = base64.encodestring(signature).replace('\n', '')
        return encoded

    def __generate_signagture(self, timestamp):
        data = str(self.customer_id) + "&" + str(timestamp)
        return self.__generate_hmac(data)


    def __generate_headers(self, data_format='json'):
        """
        generate header data required by SepWeb
        :param data_format:
        :return:
        """
        timestamp = self.__generate_timestamp()
        signature = self.__generate_signagture(timestamp)
        headers = {
            "X-cons-id": self.customer_id,
            "X-timestamp": timestamp,
            "X-signature": signature
        }
        if data_format == 'json':
            headers['Accept'] = 'application/json'
        elif data_format == 'xml':
            headers['Accept'] = "text/xml"
        else:
            headers['Accept'] = 'application/json'
        return headers

    def search_peserta_based_kartu(self, no_bpjs, data_format='json'):
        """
        pencarian peserta bpjs berdasarkan nomor bpjs

        deskripsi detil:
        https://docs.google.com/document/d/1vydifb2Kde3fPAMZn7yyrduF7WA0eZZlhkpExQzgw_c/pub#h.1a96yyehn3d9

        :param no_bpjs:
        :return: data peserta bpjs dalam format json/xml
        """
        url = self.BASE_URL + '/peserta/' + no_bpjs
        headers = self.__generate_headers(data_format)
        req = requests.get(url, headers=headers)
        return req.text


    def search_peserta_based_nik(self, nik, data_format='json'):
        """
        Search informasi perserta BPJS berdasarkan Nomor Induk Kependudukan

        deskripsi detil:
        https://docs.google.com/document/d/1vydifb2Kde3fPAMZn7yyrduF7WA0eZZlhkpExQzgw_c/pub#h.dxr94pns13zw
        :param nik:
        :return: data peserta bpjs dalam format json/xml
        """
        url = self.BASE_URL + "/peserta/nik/" + nik
        headers = self.__generate_headers(data_format=data_format)
        req = requests.get(url, headers=headers)
        return req.text

    def search_rujukan(self, nomor_rujukan):
        """
        Mencari data rujukan berdasarkan nomor rujukan

        deskripsi detil:
        https://docs.google.com/document/d/1vydifb2Kde3fPAMZn7yyrduF7WA0eZZlhkpExQzgw_c/pub#h.kq6eb079ur9j
        :param nomor_rujukan:
        :return:
        """
        url = self.BASE_URL + "/rujukan/" + nomor_rujukan
        headers = self.__generate_headers()
        req = requests.get(url, headers=headers)
        return req.text

    def search_rujukan_based_bpjs(self, nomor_bpjs):
        """
        Mencari data rujukan berdasarkan nomor bpjs peserta

        deskripsi detil ada di:
        https://docs.google.com/document/d/1vydifb2Kde3fPAMZn7yyrduF7WA0eZZlhkpExQzgw_c/pub#h.jb8j6882s535
        :param nomor_bpjs:
        :return:
        """
        url = self.BASE_URL + "/rujukan/peserta/" + nomor_bpjs
        headers = self.__generate_headers()
        req = requests.get(url, headers=headers)
        return req.text

    def search_daftar_pasien_based_date(self, start_date=None, start=1, limit=10):
        """
        Pencarian daftar pasien berdasarkan tanggal masuk.

        deskripsidetil ada di:
        https://docs.google.com/document/d/1vydifb2Kde3fPAMZn7yyrduF7WA0eZZlhkpExQzgw_c/pub#h.tsg51s1bnl56
        :param start_date:
        :param start: data awal
        :param limit: batasan query
        :return: list pasien rujukan
        """
        url = self.BASE_URL + '/rujukan/tglrujuk/'

        if start_date:
            date = start_date
        else:
            date = datetime.datetime.utcnow()
        year = str(date).split(' ')[0]
        url += year + '/query?start=' + str(start) + '&limit=' + str(limit)

        headers = self.__generate_headers()
        req = requests.get(url, headers=headers)
        return req.text

    def sep(self, xml_data):
        url = self.BASE_URL + '/sep/create/'
        headers = self.__generate_headers()
        headers['Content-Type'] = 'application/xml'

        req = requests.post(
            url,
            data=xml_data,
            headers=headers
        )
        return req.text
