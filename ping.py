from __future__ import annotations

import time

from scapy.all import TCP, IP, sr1, Packet
from typing import Optional, Iterator
from dataclasses import dataclass
from itertools import count


def start_ping(*args, **kwargs):
    """Сигнатуру функции желательно поменять"""
    # TODO: Создай функцию, которая будет доставать пакеты из пингового
    # TODO: генератора и выводить их, а по завершении выводить статистику
    pass


class Ping:
    def __init__(self, ip: str, port: int = 80,
                 timeout: int = 1,
                 interval: Optional[int] = None):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.interval = interval

    def _send_syn(self, seq: int) -> Optional[Packet]:
        packet = IP(dst=self.ip) / TCP(dport=self.port, flags="S", seq=seq)
        return sr1(packet, timeout=self.timeout, verbose=0)

    def ping(self, itr_count: Optional[int] = None) -> Iterator[PingResponse]:
        for seq in count(0, 1):
            packet = self._send_syn(seq)
            if _is_rst_response(packet):
                raise ConnectionRefusedError
            if packet:
                yield PingResponse.from_packet(packet)
            if count and seq >= itr_count:
                break
            if self.timeout:
                time.sleep(self.timeout)


@dataclass
class PingResponse:
    length: int
    seq: int
    ttl: int
    rtt: float
    ip: str

    @classmethod
    def from_packet(cls, packet: Packet) -> PingResponse:
        return cls(
            length=packet[IP].len,
            seq=packet[TCP].seq,
            ttl=packet[IP].ttl,
            rtt=packet.time,
            ip=packet[IP].src,
        )

    def __str__(self) -> str:
        return (
            f"{self.length} bytes from {self.ip}: "
            f"tcp_seq={self.seq} ttl={self.ttl} time={self.rtt} ms"
        )


def _is_rst_response(response: Optional[Packet]) -> bool:
    return response is not None and response[TCP].flags == "RA"
