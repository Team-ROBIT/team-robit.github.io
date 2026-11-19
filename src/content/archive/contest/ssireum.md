---
title: "SEOUL TECH 지능로봇대회 씨름로봇"
description: "상대 로봇을 경기장 밖으로 밀어내는 지능형 씨름로봇 대회"
subtitle: "SRC·IRC Ssireum Robot"
chips: ["2011년부터 참가", "2018 — 2021 4연속 우승", "2025 1위 · 4위"]
highlight: "2026 2위 · 3위"
cover: ../../../assets/assets_contest/ssireum-001.webp
coverKind: photo
sidebar: false
---

## SRCIRC 씨름로봇

![](../../../assets/assets_contest/ssireum-001.webp)

SRCIRC 씨름로봇 대회는 서울과학기술대학교에서 주최하는 지능로봇 대회로, 경기장 내에서 자율적으로 서로를 감지하여 상대방을 먼저 밀어내는 로봇이 승리하는 대회입니다.

ROBIT은 2011년도부터 꾸준히 씨름로봇 대회에 참여해 왔으며,

2018년부터 2021년도까지 4연속 우승의 쾌거를 이루어내기도 하였습니다.

![](../../../assets/assets_contest/ssireum-002.webp)

![](../../../assets/assets_contest/ssireum-003.webp)

## 2026 시즌

- **결과**: 2위, 3위
- 2개 팀이 출전했습니다.

## 2025 시즌

- **결과**: 1위, 4위

## 사용된 기술

![PSD 센서](../../../assets/assets_contest/ssireum-004.webp "PSD 센서 | 상대 로봇을 감지하기 위해 거리감지 센서인 PSD센서를 사용합니다. 보통 로봇의 모든 방향에 부착하여 적을 찾는 다양한 알고리즘을 구현합니다.")

![적외선 센서](../../../assets/assets_contest/ssireum-005.webp "적외선 센서 | 씨름 로봇은 경기장 밖으로 나가는 것을 방지하기 위해 적외선 센서를 활용해 경기장의 흰색 선을 감지합니다. 일반적으로 로봇의 전면 하단에 2개의 센서를 부착하며, 사용하는 알고리즘에 따라 후면에도 2개의 센서를 추가로 장착하기도 합니다.")

![카메라 센서](../../../assets/assets_contest/ssireum-006.webp "카메라 센서 | 2021년도 씨름로봇부터 적용된 영상처리 룰을 대비하기 위해 사용된 카메라 센서입니다. 별도의 PC를 거치지 않아도 카메라 내부에서 자체적으로 영상처리가 진행되며, 그 결과값을 UART, ADC등을 통해 MCU로 전송할 수 있습니다.")
