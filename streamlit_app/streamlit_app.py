import streamlit as st
import json
import pandas as pd
import plotly.express as px
import numpy as np
from collections import defaultdict
import time as my_time
from datetime import datetime, timedelta, time, date
from st_aggrid import AgGrid, JsCode, ColumnsAutoSizeMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


st.set_page_config(
    page_title='Росатом, алгоритм "Емеля"',
    page_icon="streamlit_app/images/favicon.png",
    layout="wide",
)  # layout = "wide"

with open("streamlit_app/css/AG_GRID_LOCALE_RU.txt", "r") as f:
    AG_CRID_LOCALE_RU = json.load(f)

col1, col2 = st.columns([1, 5])
col1.markdown(
    """<p><img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBQSFBcSFBUXFxUXFxsbGBoaFxcaGxcaGhsaGxcdFxodIiwkGx4qHhcXJjYmKS4wNDQzGyQ5PjkxPS4zMzIBCwsLEA4QHhISHjMpIicyOz09Mjg7MjQ0NDIyMjA0NDIwNT0yMDQyMjIyMjIyNDIzMjIyMjQyMDQyMjI0MD0wMv/AABEIAGUB9AMBIgACEQEDEQH/xAAcAAEAAgMBAQEAAAAAAAAAAAAABgcEBQgDAQL/xABLEAACAQMABQgGBgYGCgMAAAABAgMABBEFBhIhMQcTIkFRYXGBFDJSkZKhQmJygrHBIzWTorKzFjM0U4PCFRdDVHN0o9HT8GPD0v/EABkBAQADAQEAAAAAAAAAAAAAAAADBAUCAf/EACgRAQACAgEEAQQBBQAAAAAAAAABAgMRBBIhMUEiUWGR8HETFCMyQv/aAAwDAQACEQMRAD8AualK8Lu5SJGkkYKijLMeAFB7VGNN65W1tlQwdx1Bgqg97H8s1X+tmu010WjhLRW/DA3PJ3uR6o+qPPPAQp06zxq9i4nu34V75ZntX8rB0hr7NISFmjjXsXZ+bNk+7FaWfScr72mkcHtkdh+NRJ0r8IzIcqSD3fn21brStfEILUm3/UpIblxvDuD3Mw/OvaDWG7iOUuZR3Fy6/C+V+Va+xEssbyiNzGmNtwp2Bk49bgDvGR1Zrxc11MVs4iLVlOdF8ps0ZC3MayL1snQfxweix7ujVgaE1ht71dqCQMR6yHc6faQ78d/A9Rrn9zX4huHidZI3ZHU5VlJDA9x/Lrqtk4tbf69pWKZZjy6bpVf6ja/LdkW1zspccFYbkm8B9F/q8DxHYLArPvSazqVmJ2+0pSuXpSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKD8mqj131gN3JzUZ/QId2PpsOLHtHs+/r3TzXG4kW2ZYkZmfosVUnZU+sTjhu3efdVTPHV7h4on5Sp8nLMfGGtdK8HSti8deLpV+YVq3a50qT6janG/kMkuVtkOGxkGVuOwp6h7TDtwN5yus0fo17mWOBPWdgoPYOLMe4KCT4VfOi7FLaJIIxhEXA7T2k9pJySe0mqnJy9EajzK1hr1d/T9w2caRiFUVYwuyECgKF4Y2eGKpTXbQBsZ9lc8zJloz2DPSQntUkeRXrzV6VH9cdHW9xb7NyzIiurB1GWVuAxuO4gkHd11TwZZpb+U2SsTG/ooNzXixqwm1U0ZxN9Nj/AIe/+D8q9YrDQ9tvWKW7ccOdOF+8uFBHihrQ/q78RP4V4tWPMwh2rerFzfMDHmOJTl52yFTZOcod204xwB3HGSvGry0JpeKbMCSGRolUF2xmQAAFxjAO/iQAMnduIqu9LaxSzrzfRSIbhGg2VwOAPteHDurXaN0q1tMky79g7x7Sncy+Yz54PVXGTBbJXdvPqHn9zEWiK+F4Urxt5lkRXU5V1DKR1hhkH3GvasxeKUqgOUZB/pS63D1o/wCRFQX/AErlvmx2D3V9CDsFB1HSubbHTl1AQYriVMdQkYr5o2VPmKsnUzlEM7rbXYVXchY5V3K7Hgrr9Fj1EbiTjA3ZCyaUpQK85JFUZZgo7SQB7zVca6coZidraz2S6krJKQGVGG4qinczDrJ3AjGDvxWF/eyXDc5NI8rdrsWxnsz6o7huoOh/6QWedn0q3z2c9Hn3bVZ0MyONpGVh2qQR7xXMWK9bW5kibbjd439pGKN71xQdO0qqdUeUhgywXxBUkBZ8Bdk9XOgbtn64xjrGMsLWoFKVh6Rvo7eNppWCIgyzHq7N3EknAAG8kgUGZXhPcpGMu6oO1mCj51TesnKLc3DFLYmCLgCMc647Wb6Hgu8e0ahMzl2LuS7HizEsx8WO80HRv9IbPOPS7fPZz8efdtVnwzI42kZWHapBHvFcxYr0tHkRwYWdJCQFKMUYknAAZSDxxQdPUrHtYyiIjMXZVVSx4sQACT3njWRQKUrnfXTSIu72aXiofm4+B6EfRGO4kM336Doilct82Owe6rl5I9Jc5aNbk9KCQ4H1JMuv73ODwUUE/pSqT5XkBv1yB/Zo/wCOaguylct82Owe6nNjsHuoOpKVy3zY7B7qc2Owe6g6kpVSci6gS3WAP6uL+KSrZJxvPCg/VeM9wiDadlUdrMFHvNVXrbykOzNDYkKg3GbAJft5oHcF+sck9WNxNd3M7yttyO0jn6TsXb4myaDopdP2ZOyLq3J7BNHn3bVbCN1YbSkEHrBBHvFcw4rJsL+W3bbhkeJuOUYrn7QG5h3HIoOmaVW+pXKFz7LbXeysjECOUAKsjdSuOCueojcTuwDgGyKBSlVJy0OGltUP0Y5G+Jox/koLbpXLfNjsHuq6OSTSHOWbQHjBIQB9R+mp+IyD7tBPKUrynlVFZ2OFVSzHsAGSfcKD1pXMd/cGeWSdh0pJGc53422LY8s48qzNWHCXlq4A3XEQ8mdVb5E0HSFKUoKX121xu4dIyrbTMiRBE2OiyOQNtyVYEZy5UkYPRG+snRus1rpEiK8Rba5O5Z03I7dQcH1c/WJH1gSBUG0s+3cTP7c0j/E7H86xNitSuGIrGu0/VWtaLdp8J1pfRMls5jkHerD1XHap/LqrVPHW+1M0oL2I6NuGzIqlrWRt5BUZKE8TgDd9UEfRFYU1owcoVO2G2dnr2s4x3nO6pcd5ntbzH7tSy4+mdx4lJeTHRY2pLlh6v6NPE4Zz7tgZ8asYmtXq9o30a3SL6QGW+0xy3iATgdwFQXWLWZ7iV4kcpCjFeicFyNxZiN+znOBwxvPdnzWc+SdLvVGHHG/KzgawNNWHpEDxcCy7j2MCCufMCqSlmaJtuJ2jbjtIxU+8casvk+1pa+jeOXHPxY2iBgOjZ2WwNwOQQQN3A7s4HuXj2xfKJ3p7jyxljUwgFwWRijAqykhgeII3EGsV5asfXjVrnlNzCP0qjpqP9ooHUPbA4do3dlVY0lX8OaMldwpZMM1tp7PJXk714vJXi8lSbK41x8m+kOdtObJ6ULsn3Th08gG2fu1L6q7kgnPOXKdRWNvMGQH8R7qtGsjkV6cktHHO6w+1QXKL+s7r7Uf8iKr9qguUX9Z3X2o/5EVQpHrydaIgvLtorhNtBA7gbTp0g8ag5Ug8Hbd31ZbcnejCP6hh4TT/AJvUD5If7e//AC0n8yGrpoKX161GWxj9Jgdmi2grq+C0e0cKQwxtLkhcEZBI3nO6C/8Au7j5VeHKheJHo+SNiNqVkVF6yQ6uxHgqk57cdtUfQdFaq6QNzZwTscs8a7Z7XXoufiU1qeUbTrWdoRGcSzHYQjioxmRx4LuB6iy1k8nsJTRtsD1ozjwd2dfkwqA8sV0Wu4ouqOHaHjI7BvlElBAAMVYuo2oCXEa3d3nYcZjiBK7S9TyMN+DxAGN2CTvwIJoq05+eKE8JZY0OOpXcKx8gSa6UjQKAoGABgAcABwAoNP8A0S0fjZ9Dt/HmUz8WM/OoTrjydRrG1xZhlKAs8OSwYDeTETkhvq5IPAY67SpQcu1c/JXpw3Fs1u5zJbkKCeJjbPN58Nll8FXtqrdaLIW95cQruVZW2R2K/TUDwVgPKt/yT3RS/wBjO6WJ1x2lSrg+QVveaC7qpnlV0801x6Ih/RwYLjqeRhnf27KkAd5arkJxvNcy3d0ZpJJjxldpD4uxY/jQfiGJpGWNFLOxCqoGSzE4AA7c1amr/JfGFD3jM7kb40bZRe5mHSY94IHjxrT8kWjFkuZbhhnmEUJnqeTaG0O8KjD79XHQRtNSNHKMC1j8y5PxEk1jrqBYJJHNHG8bRyLIAsjlSykMAVYndkDcMVLKUClKUGi1x0p6JZzTA4cJsx/bfoIfItnwBrnngPAVZ/LHpPJhtFPDMrj3pH/9nyqH6kaN9KvoEIyqvtv9mPp7+4sFX71B7a56umxa3GP6y3Qv/wAVN02O7pIfOsrkx0nzF8iE4SdTGeza9aM+OV2R9up5yraN52y50DpQSK/fsN0HHh0lY/Yql4ZWjZZEOHRgynsZSGU+8Cg6gqO6c1PtL2UTTq5cIEyJHUbKlmG4HHF2ra6KvVuIY509WRFcd20AcHvHDyrNoIb/AKtdHf3cn7WT/vVU64aOS1vZreIERxlNkElj0o0c5J3nexroiqD5Rv1nc+Mf8iKg/OoOh4ry75mYEx8074DFTtKUA3j7RqzP9Wujv7uT9rJ/3qCckv6w/wACT+JKu2g0WgNV7awLtbqymQKG2nZshSSMZO71jUa5V9OGGBbWM4efO2R1RLuYfeJA8AwqwqonlOujJpGVeqNEQeGwJD+9K1BEycVauqHJzHzaz3ql5GAZYslVjB3jbxvZu0cBwweNQbUqxFxf28bDK85tt2YjVnwe4lAPOuhqDRNqlo8jHocA7xEoPxAZ+dV3rzqCttG11a7RiXfJGxLGMe0jHeVHWDkjjnHC4a8Z4ldWRgCrAhgeBBGCD5Gg5jq+eT/ThvLNWc5ljJjkPWzKAQx72UqT35qi7u35qSSInJjkdCe0oxUn5VYXI3ckS3EWdzIjgd6MVJ/6i+4UFt1SvK5LtXyr1LboPMvIT8itXVVC8pM23pKcdSc2o/Zox+bGgi9Tbko0jzV6YiejPGV8XTLp+6JR51GtGaNM0dy44wRCTy20DZ8EMh8qx9G3pt5Yp1zmKRXwOvZIJHmAR50HTNRLlM0jzGj5VBw0xES94fJkH7NZKlMUgdQynKsAQe0EZBqpuWLSO1NDbA7o0Lt2FnOyvmAjfHQV1X7t5ubdJPYZX+EhvyrOsdGmS3urj6MCxebSSog/d5z5VrXGQR3UHUVfawtEzc7BDJ7cSN8Sg/nSg5znjIdgeIYg+RNfgJW51iszFd3CHqlcj7LMXT91lrXBK2694iVGZ7vXQ0UpuIhB/Xc4pj7NoHI2vq7t/dmr6TQ0QnNxs5kOOJyFOMEqO0jr/wC5qDclWhhl7xhw/Rx56uBdh71XP2qs2s7k5PnqE+OkTG5fDXOZkaJmifc8bFGHYyHZb5g10bUG1y1BS+c3ETiGc42iV2kkwMAsOKtgAbQ6hvB3Y542WMczv26y4+uFR3F1mplyNws13PKM7CQ7B7CzurL5gRt768rXknvGfEs8CJ1lDJI3kpVB86tLV7QcNjCIIQcA5ZjvZ2OMs56zuHcAABuFT589Zr0xO9vMePpbaqd5R9B+jTCeMYimJ3DgknFh4MMsPvdQFXFWi1x0X6XZzRAZfYLR/bTpJ4ZIx4E1VwZOi+/TvJXqhQrvXiz15GTO+v1bxmRwi9fE9g6zWuq9Oo3KzeSCIhpX9pfkGAHzDVadQXkztgqSsB0cqi/dBJ/iWp1WVyZ/ySnwd67faoLlF/Wd19qP+RFV+1QXKL+s7r7Uf8iKoEzWaC01NZSGaAqHKFDtLtDZYqx3duUWt7JykaRYYDxr3rEuR4bWR8q1GrGgmv5/R0dUPNs+0wJGFKjGB9r5VL15Jpuu6jHhEx/zCggWkdIzXL85PI8j8MseA7FA3KO4ACthqtq9JpCYRICIwQZX6kTr3+2eAHbv4A1YejeSq3QgzzSS4+ioEanx3s3uYVOdH6Pit0EUMaxoOCqMDPWT2k9ZO80HtBEsaqigKqgKoHAKBgAeQql+VlcaQ8YIyPDacfiDV3VU/LJYESW90BuZWiY96kvGPMGX3UEO1QcLfWpPDn4x5sdkfMiuia5fhlaNlkQ4dGDKexlIKn3gV0boHSyXkCXEfBxvHWrD1lbvByKDZ0pWLf3iQRvNI2yiKWY9gH4nu66CieUFgdJXRHtoPdFGD8wayOTNCdJQkdQkJ8ObcfiRUe0jeNPLLO25pZHcjjjaYkDyBA8qm/I/YF7qaf6McWx96RgRg9yxt8QoLbugSj447LY9xrmKP1R4CupK5r03YG2uZrcjHNyMoH1M5jPmhU+dBYvIxINm6TrDRt5EOB81NWfVB6g6fWxuwznEMi7Eh9nflH8juPczGr4jcMAVIIIyCDkEHgQesUHpSlKBSlR/XfSnotlNKDhyuwnbtSdEEeGS33aCldbNKelXk0wOVLlY9+RsJ0EI7iF2vvGpnyQ28ac/dSMik4iTaYA4GHk4ngcxfCarQCvhUdlB0hfy288TwvJHsSIyN014MCD199c5zRGNmjbG0jFWxvGVJBwesZFeeyOwV9oLi5I9J85avbk9KB9w+pJll/f5weQqwKonkz0n6PfopOEnBiPZtHpRnx2lCj7Zq9qBVB8o36zufGP+RFV+VQfKN+s7nxj/AJEVBn8kv6w/wJP4kq7apLkl/WH+BJ/ElXbQK5/5QBjSV0Prp844yPka6AqleVqxMd6suOjNEDntdOg/uXmvfQYXJlIBpKEH6SyAePNsfwU1e9c06Hv2tZ47hRkxyBse0B6y+alh510ZY3iTRrLGwZHUFWHWD+HhQZVKVqtYNLJZ28lw/wBFTsj2nO5FHicfM0FA6ebN3ckcDczEeBkcipdyPIfTZT1C3YHxMkePwNQMsScsck7ye0niT51aXI3YkLcXB4MUjX7oLP4jpp7jQWfXOut8/OX103/zSL8B5v8AyV0VXM2kZucmlk9uWR/idm/OgnnJFaLKb1XGUaONGHar84GHuWoDe2rQySQv60bsjdWSjFSfA4z51aHIzF+iuX7ZEX4VJ/z1G+VTR3M3xkA6M6K/316DgeSofvUFh8m+kef0fECelFmJu7Y9T9wp76p/WvSHpV5PMDlWkITfu2E6CEeKqD51udStY/RIL2PawWh24u6TIjHiSZIz4IailpbNI8cKetI6ovi5Cr8yKCytEaI2NAXDkdKZXmP2UI2PLZjDfeqsa6I0zYKuj5rdBhVtZI0HYBGVX8BXO4NB0JqRNtaPtT2QovwDZ/y0rXcl8m1o2Iey0q/9R2HyYUoIzyn6L2J0uAOjKuyx+unDPimPgNQkJV66x6JW7t3hOAx3ox+i49U+HUe4mqVlt2RmR1KupIZTxBG4itPi36qa9wociJrbfqW51U5Q/Q19Fmh2okZtlo8B1yxJ2lY4feSc5B7jVgWWvOjpRuuUQ9kgaMj4wAfI1QUyYkcfWP416x15fi1tO08XmsRp0R/SWy/3y2/bR/8A6rwn1usU43CN9jaf+AGqKirNjryOFX3Mo78iY8QtaTX63zhElbv2VA+bZ+VZ+itaoLhwgDozblDKCCeO4qT1DrxVUQVJkuxo6ya8wOfmOxbgjOzx2nI8ie/Cj6VeZeNSle3lxiz5L2+y0a8pZlQbTMqjtJAHvNc6LpGUkkyykk5J5x95O8k76/O3tHaY5Pad595riOF9bJ5z/ZjPYMZHC4WMOwU/VDHZwPDFbazhWMYXzJ4nxrxVqlOo+hTdXAZh+iiIZ+xm+ivfkjJ7ge0Vem0Ur1T6VbdWSemFkaqaPNvaxqww7DaftDNvwe8DC+VbqvlfaxbTNpmZaFaxWIiH2qC5Rf1ndfaj/kRVftVbrZqBeXd5NcxvAI3KFQ8kgboxxocgIRxQ9deOml5Jf1gf+Xk/jjq7KrjUXUm6sbozzNCU5p0wjuzZZlI3NGox0T11Y9ApSlArUayaGS9tpLdzjaGUb2HG9G9/EdYJHXW3pQczaRsJLaR4ZVKSIcMPwKnrU8Qeus7V/WK5sHLwOMN66MNpHxwJXIIPeCD5Vd+sWrNtfoFmTpKDsSLudM9h6x9UgjuquNJclt0hJglilXq2sxv3DG9T45HhQZicrUmN9mhbtE5A+Hmz+NRXWXW+50hhZCqRA5EaZC5HAuTvcj3dwr2PJ/pPOPRvPnYMfx5raaP5LrxyOdkiiXr3mRx90YU/FQQi3geR1jRS7udlFXeWJ6h/7u41f2pugRYWyw7jIx25SOBdgMgdwACjuXPXX41Z1RtrAZjUtKRhpXwXx1hcbkXuHHAznFSOgVW3Kjqs0wF7CpZ0XZlQDeyD1XUdZXeD2jHs4Nk0oOXQa3ugdbbyyGxFJlP7uQbaD7IyGXwUgb6s7WTk7trktJEfR5WySVUFGJ4lk3YPepHEk5qEXnJnfoTsCKQdWw+yT4hwAD5mg2CcrFxjfbxE9oZwPdv/ABrDHKVePNEXaKOISIZFRPWj2hthmcsfVzvGK1y8n+kycejY7zLBj5OTW30dyWXTn9PLFGnXs5kfvGMBR45PhQXJVT8sWk9p4bQHcgMrjvbKR+YAl+IVaNvHsIq5LbKgZOMtgYycbsmqv1j1Cv7y6luNu2Cu/QBklyEUBUBHNEA7KjIHWTQQnVbRvpd5DARlWkBf7CdOQHsyqkeJFXd/Q7R/+6Q/BUe1A1JmsJpJ7ho2YoETm2ZsbTZcttIuPVXGM8W4ddgUGg/odo//AHSH4Kh/KVqtbw2q3FvCkRjkUSbAxlH6Iz24cp7zVn1gaYsFuYJbdtwlRlz2EjAPiDg+VBzdHIyMrocOrBlPYynKnyIFdJaIvluYIp14SRq+OzaAJB7wcjyqoxyW3/t2v7WX/wAVWLqNom4s7X0e4MbFHYxmNmI2G6WDtKu/aL+RFBJaoPlG/Wdz4x/yIqvyqt1t1AvLy8muY2gEblNkO8gboxohyBGQN6nroNJyS/rD/Ak/iSrtquNRdSbqxuufmaEpzTphHdmyxQjc0ajHRPXVj0Co3rvq7/pC2KLgSoduIncNoAgqx9lgSO44PVUkpQcwTwtGzRupR0JVlYYKkcQRW81b1tutH5WNg0ZOTG4JXPWVwQUPhu7Qat7WfU+20h0pAUlAwJUwGwOAcHc6+O8b8EZqvL/kvvEJ5p4pV6t5Rj4q2QPiNBsTytPj+xrtdvPnHu5v86hmsWslxfuGmYbK+pGgKomesDJJbHWSTxxgbqzxyf6TJx6NjvMsGPk+a3OjOSy6cgzyxxL2Jl27xjAUeOT4UEJ0Zo+S6lSCFdqRzuHUB1sx6lHEn88CuhdAaJSzt47ZN4Rd54FmJy7HxJJrH1e1bt7BCsKdJsbbtvd8cNpuzuAA47q3dB4XcuxG7+yjN7gT+VcxRjAA7hXSem7Z5raaKMqHkidELEgBnUqpJAJAyew1U3+qy/8Abtf2kv8A4qCWcj8WzZyN7dwx8gka/iDXzlc0dzlos4HSgkGT9STCMB97mz5VvdSdCyWNosEpQuHdmKFivSYkYLAHhjqraaYsRcwSwNuEkbJnsLAgHyOD5UHNdTHkt0dz18shHRgRnPZtHoID8TMPsV7jktv/AG7X9rL/AOKpzyfarSaPjl54xmWRxvQsw2FHQGWVTnaaQ8OsUEsuI9tGX2lI94xXMEfAeArqSqYm5Lr0sxVrbZLNs5klzs5Ozn9HxxigkPJNpBVs5FY8LhseBSM/iTX2sXQmpekLZGj27Xe5b+sl6wB/dd1fKCz6huuerHP5uYR+lA6Sj/aAcCPrAe8buoVMqGuqXmltw4vSLxqXNum7Uq4kA3NuPcw7fIfKsOOr11l1RjuwzJhJG9b2X+1jgfrD51T+mNBzWT7EqFQT0WI3N4Ebia1MeauTx5+irNbVjpn8seKsyOsOKs2Op4QXbCzjLsqDixCjxJwPxr15ULsG6S2X1LWJFA7GcBm96c17q9dBf2iDPDno/wCNa0mv5P8ApK7z7afyo8fLFRX75I+0JOPHxlpkavdGrEVql2rGpV1eEMymGH22BBYf/GnFvE4HeeFe2vFY3Mu+mZ8MLQei5buUQxDJO9mPqxr1sx7O7rq79CaJjtIVhj4DexPF2PrM3efkMDgK/OhNCw2cYihXA4sx3s59pz1n5DgABW0rNz55yTqPCxjxxXv7faUpUCUpSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlArwubVJkKSIrqeKsAQfEGvlKCJX/J1aOdqMyQnsVtpfhbJHkRUX0tqibX/AG+3/h7P+c0pVzj5b9WtqualdeGFo22O2CGwVIIOM7wRjrqW6w8nUd9dvcvO6K6ptKiLkso2drbYkeqqjGz1UpXfKvaLRMfvhxxY7S2+hNSbG0IZIg8g4PIdtge1c7kP2QKktKVRtaZnuuQ+0pSvHpSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKBSlKD//2Q==" width="280" height="50" align="middle" /> </p>""",
    unsafe_allow_html=True,
)
col2.markdown(
    '<p style="text-align: center; font-size:20px; color: blac;"><STRONG>Алгоритм "Емеля"</STRONG></p>',
    unsafe_allow_html=True,
)
col2.markdown(
    "<p style='text-align: center; color: blac;'> ИИ оптимизирует производство атомного топлива </p>",
    unsafe_allow_html=True,
)

st.write("##")


def load_json_file(uploaded_file):
    day = json.load(uploaded_file)
    return day


def get_operation(operations: list) -> dict:
    return {operation: 1 for operation in operations}


def make_ovens_df_from_json(day):
    data = []
    for i in range(len(day["ovens"])):
        data_dict = defaultdict(dict)
        data_dict["start_temp"] = day["ovens"][i]["start_temp"]
        data_dict["working_temps"] = day["ovens"][i]["working_temps"]
        data_dict.update(get_operation(day["ovens"][i]["operations"]))
        data_dict.update({"oven": i})
        data.append(data_dict)
    df = pd.DataFrame(data)
    df.fillna(0, inplace=True)
    df["prokat"] = df["prokat"].astype("int")
    df["kovka"] = df["kovka"].astype("int")
    df["otzhig"] = df["otzhig"].astype("int")

    return df


def make_series_df_from_json(day):
    data = []
    # for i in range(len(day["series"])):
    #     data_dict = defaultdict(dict)
    #     data_dict["temperature"] = day["series"][i]["temperature"]
    #     for operation in day["series"][i]["operations"]:
    #         data_dict[operation["name"]] = operation["timing"]
    #     data_dict.update({"series": i})
    #     data.append(data_dict)
    # df = pd.DataFrame(data)
    # df.fillna(0, inplace=True)

    for i in range(len(day["series"])):
        for operation in day["series"][i]["operations"]:
            data_dict = defaultdict(dict)
            data_dict["temperature"] = day["series"][i]["temperature"]
            data_dict[operation["name"]] = operation["timing"]
            data_dict.update({"series": i})
            data.append(data_dict)

    df = pd.DataFrame(data)
    df.fillna(0, inplace=True)

    return df


operation_dict = {0: "prokat", 1: "otzhig", 2: "kovka"}
operation_list = np.array(["prokat", "otzhig", "kovka"])

data_dict = {"oven" : "Номер печи",
             "series" : "Номер серии",
             "temp" : "Температура в печи",
             "operation" : "Наименование операции",
             "timing" : "Продолжительность операции, мин",
             "total_timing" : "Текущее время"}


def algoritm_emelya(df_series, df_ovens):
    # план на день
    data_ovens = []
    # время на начало дня
    t = time(0, 0)
    dt = datetime.combine(date.today(), t)
    # время на конец дня
    t_end = time(23, 59, 59)
    dt_end = datetime.combine(date.today(), t_end)
    oven_timing = defaultdict()
    # распределенные серии
    series_trye = []
    # распределенные печей
    ovens_trye = set()
    # проход по сериям в порядке приоритета
    for i in list(map(int, df_series["series"].unique())):
        # выборка текущей серии
        df_series_now = df_series.iloc[np.where(df_series["series"] == i)[0], :]
        # перечень операций в текущей серии
        operation_series_now = operation_list[
            df_series_now.iloc[:, [3, 4, 5]].sum() > 0
        ]
        # выбор подходящей печи по температуре и доступным операциям
        try:
            oven_index = np.where(
                (df_ovens["start_temp"] == df_series_now["temperature"].unique()[0])
                & (df_ovens[operation_series_now].sum(axis=1) == len(operation_series_now))
            )[0][0]
       
        except:
            continue
        # фиксация начала дня
        if not oven_timing.get(oven_index):
            data_dict = defaultdict(dict)
             # номер печи
            data_dict.update({"oven": str(oven_index)})
            # данные серии
            data_dict.update({"series": "-"})
            # температура печи
            data_dict.update({"temp": df_ovens.loc[oven_index]["start_temp"]})
            # операция в печи
            data_dict.update({"operation": "start_day"})
            # продолжительность операции в минутах
            data_dict.update({"timing": 0})
            # текущее время
            data_dict.update({"total_timing": dt})
            # добавление в план
            data_ovens.append(data_dict)
            # текущее время в печи
            oven_timing[oven_index] = dt
        # операции прогрева
        progrev_false = 1  # len(df_series_now)
        total_time_for_series = df_series_now.iloc[:, [1, 3, 4, 5]].sum().sum() + (len(df_series_now) - 2) * 120 + 15
        if oven_timing[oven_index] + timedelta(minutes=int(total_time_for_series)) <= dt_end:
            ovens_trye.add(oven_index)
        else:
            continue
        series_trye.append(i)
        # планирование операции серии в печи
        for temperature, nagrev, series, prokat, otzhig, kovka in df_series_now.values:
            if nagrev > 0:
                data_dict = defaultdict(dict)
                # текущий день
                # data_dict.update({"day" : 0})
                # номер печи
                data_dict.update({"oven": str(oven_index)})
                # данные серии
                data_dict.update({"series": series})
                # температура печи
                data_dict.update({"temp": temperature})
                # операция в печи
                data_dict.update({"operation": "nagrev"})
                # продолжительность операции в минутах
                data_dict.update({"timing": nagrev})
                # текущее время в печи
                oven_timing[oven_index] = oven_timing[oven_index] + timedelta(minutes=int(nagrev))
                # текущее время
                data_dict.update({"total_timing": oven_timing[oven_index]})
                # планирование операции серии в печи
                data_ovens.append(data_dict)
            else:
                # распределение операции
                data_dict = defaultdict(dict)
                # текущий день
                # data_dict.update({"day" : 0})
                # номер печи
                data_dict.update({"oven": str(oven_index)})
                # данные серии
                data_dict.update({"series": series})
                # температура печи
                data_dict.update({"temp": temperature})
                # операция в печи
                data_dict.update(
                    {
                        "operation": operation_dict.get(
                            np.argmax([prokat, otzhig, kovka])
                        )
                    }
                )
                # продолжительность операции в минутах
                data_dict.update({"timing": max(prokat, otzhig, kovka)})
                # текущее время в печи
                oven_timing[oven_index] = oven_timing[oven_index] + timedelta(
                    minutes=max(prokat, otzhig, kovka)
                )
                # текущее время
                data_dict.update({"total_timing": oven_timing[oven_index]})
                # планирование операции серии в печи
                data_ovens.append(data_dict)
                progrev_false += 1
                if progrev_false < len(df_series_now):
                    # фиксация прогрева
                    data_dict = defaultdict(dict)
                    # текущий день
                    # data_dict.update({"day" : 0})
                    # номер печи
                    data_dict.update({"oven": str(oven_index)})
                    # данные серии
                    data_dict.update({"series": series})
                    # температура печи
                    data_dict.update({"temp": temperature})
                    # операция в печи
                    data_dict.update({"operation": "progrev"})
                    # продолжительность операции в минутах
                    data_dict.update({"timing": 120})
                    # текущее время в печи
                    oven_timing[oven_index] = oven_timing[oven_index] + timedelta(
                        minutes=120
                    )
                    # текущее время
                    data_dict.update({"total_timing": oven_timing[oven_index]})
                    # планирование операции серии в печи
                    data_ovens.append(data_dict)
        # фиксация смены серии (технологическая пауза 15 мин)
        data_dict = defaultdict(dict)
        # текущий день
        # data_dict.update({"day" : 0})
        # номер печи
        data_dict.update({"oven": str(oven_index)})
        # данные серии
        data_dict.update({"series": "-"})
        # температура печи
        data_dict.update({"temp": temperature})
        # операция в печи
        data_dict.update({"operation": "change_series"})
        # продолжительность операции в минутах
        data_dict.update({"timing": 15})
        # текущее время в печи
        oven_timing[oven_index] = oven_timing[oven_index] + timedelta(
                        minutes=15
                    )
        # текущее время
        data_dict.update({"total_timing": oven_timing[oven_index]})
        # планирование операции серии в печи
        data_ovens.append(data_dict)

    return data_ovens, series_trye, ovens_trye


col1, col2, col3 = st.columns(3)
with col2:
    rosatom_form = st.form("rosatom")
    uploaded_file = rosatom_form.file_uploader(
        "Загрузка файла", type=["json"], help="загрузите файл"
    )
    submitted = rosatom_form.form_submit_button("Спланировать", type="primary")
    if submitted and uploaded_file:
        st.success("Файл загружен", icon="✅")
        day = load_json_file(uploaded_file)
        ovens_df = make_ovens_df_from_json(day)
        series_df = make_series_df_from_json(day)
    elif submitted and not uploaded_file:
        st.error("Загрузите файл", icon="❌")
    else:
        st.warning("Загрузите файл", icon="⚠️")

if submitted and uploaded_file:
    
    start = my_time.time() ## точка отсчета времени       
    data_ovens, series_trye, ovens_trye = algoritm_emelya(series_df, ovens_df)
    end = my_time.time() - start ## собственно время работы программы


    df = pd.DataFrame(data_ovens)
    df.rename(columns=data_dict, inplace=True)

    js = JsCode(
        """
            function(e) {
                let api = e.api;     
                let sel = api.getSelectedRows();
                api.applyTransaction({remove: sel});
            };
            """
    )

    gd = GridOptionsBuilder.from_dataframe(df, columns_auto_size_mode=0)
    gd.configure_pagination(
        enabled=True, paginationAutoPageSize=False, paginationPageSize=10
    )
    gd.configure_grid_options(stopEditingWhenCellsLoseFocus=True)  # , rowHeight=80
    gd.configure_grid_options(localeText=AG_CRID_LOCALE_RU)
    gd.configure_default_column(editable=True, groupable=True)
    gd.configure_selection(selection_mode="multiple", use_checkbox=True)
    gd.configure_grid_options(onRowSelected=js, pre_selected_rows=[])
    gridoptions = gd.build()
    st.divider()
    series_trye = str(round(len(series_trye) / len (series_df["series"].unique()) * 100, 2)) + " %"
    ovens_trye = str(round(len(ovens_trye) / len (ovens_df) * 100, 2)) + " %"
    
    st.write("### Результаты работы алгоритма")
    st.write(f"""
        
    📌 Наименование файла: {uploaded_file.name}
        
    ✔️ Распределение серий:  {series_trye}

    ✔️ Распределение печей:  {ovens_trye}

    ✔️ Время работы алгоритма:  {str(round(end, 2)) + " секунд"}

    ✔️ Минимальная загрузка печи:  {df.groupby("Номер печи")["Текущее время"].max().min()}

    ✔️ Максимальная загрузка печи:  {df["Текущее время"].max()}
       
        """)
    st.divider()
    st.write("### План на {}".format(date.today()))
    grid_table = AgGrid(
        df,
        gridOptions=gridoptions,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        theme="alpine",
    )

    if grid_table:
        df_plotly = df.copy()
        df_plotly['Текущее время'] = pd.to_datetime(df_plotly['Текущее время'])
        df_plotly['start'] = df_plotly.groupby('Номер печи')['Текущее время'].shift(1)
        df_plotly['start'] = df_plotly['start'].fillna(df_plotly['start'].min().normalize())
        df_plotly = df_plotly[df_plotly['Наименование операции'] != "start_day"]

        df_plotly = df_plotly.sort_values('Номер печи')
        df_plotly['Номер печи'] = df_plotly['Номер печи'].apply(lambda x: "№" + x)

        df_plotly['Start'] = df_plotly['start']
        df_plotly['Finish'] = df_plotly['Текущее время']
        colors = {
                    'progrev':'#ff0',
                    'change_series':'#ccc',
                    'nagrev':'#fc0',
                    'kovka':'#9c3',
                    'otzhig':'#f60',
                    'prokat':'#639'
                    }

        legends = {
        'change_series':  'Смена серии',
        'nagrev':'Нагрев',
        'progrev':'Прогрев',
        'kovka':'Ковка',
        'otzhig':'Отжиг',
        'prokat':'Прокат'
            
        }
        fig = px.timeline(df_plotly, x_start="Start", x_end="Finish", y="Номер печи", color="Наименование операции",
                    height = 800,
                color_discrete_map = colors).for_each_trace(lambda t: t.update(name = legends[t.name]))
        
        st.plotly_chart(fig, theme=None, use_container_width=True)

        df_plotly['named'] = df_plotly['Наименование операции'].map(lambda x: legends.get(x))
        fig1 = px.timeline(df_plotly[df_plotly['Наименование операции'].isin(['kovka','prokat'])], x_start="Start", 
            x_end="Finish", y="named", hover_data='Номер печи',
            color='Наименование операции',
            color_discrete_map = colors,
            height = 400, labels=dict(named="Наименование операции")).update_layout(showlegend=False)
        st.plotly_chart(fig1, theme=None, use_container_width=True)


st.write("##")
st.markdown(
    '<h5 style="text-align: center; color: blac;"> ©️ Команда "Старики разбойники" </h5>',
    unsafe_allow_html=True,
)
st.markdown(
    "<h5 style='text-align: center; color: blac;'> Цифровой прорыв 2023, Москва </h5>",
    unsafe_allow_html=True,
)
