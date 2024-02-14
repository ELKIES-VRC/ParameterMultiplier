# ParameterMultiplier

## [한국어]

### 아이디어 제공자
해당 프로젝트는 Fuuujin님의 오픈소스 프로젝트에서 영감을 받아 제작되었습니다.

아이디어 제공 및 2차 창작물에 대한 배포를 허락해주신 Fuuujin님에게 감사드립니다.

원본 프로젝트 : https://fuuujin.gumroad.com/l/OSCParameterSync?a=1061332563

### 설명
VRChat 파라미터를 256bits 이상 사용해도 다른 유저와 파라미터 동기화를 가능하게 합니다.

OSC를 사용하지 않는 방법도 있으나, 이는 차후 들어오는 유저들과 동기화를 전혀 할 수 없게 만드는 문제가 있습니다.

### 구동 테스트 환경
1. Unity 2022.3.6f1
2. Python 3.11.7

### 라이브러리
1. Modular Avatar (Modular Avatar 1.8.4 / NDMF 1.3.3)
2. Python-OSC (1.8.3)

### 사용방법
1. ParameterMultiplier.unitypackage를 Unity 프로젝트에 임포트합니다.
2. ParameterMultiplier.prefab을 아바타 최상위에 추가합니다.
3. 동기화 필요한 파라미터들을 "파라미터명,타입" 형태로 작성하여, 해당 파일을 Parameter List에 추가합니다. (동봉된 Parameter_LIST_example.txt 텍스트파일 참조)

<img width="443" alt="스크린샷 2024-02-14 133701" src="https://github.com/ELKIES-VRC/ParameterMultiplier/assets/159980894/976a3fd6-2878-4f80-9d99-28974b1322b8">

4. VRChat 접속 전, PM_OSC_Server.py 구동 후 접속 (Python-OSC 라이브러리가 설치된 Python 환경 필요)
   
* 만일 다른 사람에게 아바타가 이상하게 보인다고 들으면, Action Menu - Expressions - PM - ManualSync을 선택하세요. 모든 파라미터를 다시 동기화합니다.

### 제약사항 (알려진 이슈)
1. 아바타 리셋을 하면 VRChat 캐시 폴더 내부에 저장된 아바타 관련 저장내용이 전부 사라져 OSC 서버가 죽어버리는 문제
2. 월드 인스턴스에 접속한 이후에 들어오는 사람들에게 파라미터가 자동으로 동기화되지 않는 문제
3. 사람이 많은 환경에서 알 수 없는 이유로 모든 사람에게 완벽히 파라미터가 동기화되지 않는 문제
4. 해당 프로젝트는 실시간 동기화가 필요하지 않은 파라미터들(예 : 옷장)을 대상으로 사용하는 것을 전제로 제작되었습니다. 실시간 동기화가 필요한 (예 : 페이셜 트래킹) 파라미터에는 Sync 옵션을 사용해주세요.

## [English]

### Idea Contributor
This project was inspired by Fuuujin's open source project.

Thanks to Fuuujin for the idea and permission to distribute the secondary creation.

Original Project : https://fuuujin.gumroad.com/l/OSCParameterSync?a=1061332563

### Description
Enable parameter synchronization to other users even if the VRChat parameter is used more than 256 bits.

There is also a way to not use OSC, but there is a problem that makes it impossible to synchronize with the incoming users after you joined the instance.

### Test Environment
1. Unity 2022.3.6f1
2. Python 3.11.7

### Library
1. Modular Avatar (Modular Avatar 1.8.4 / NDMF 1.3.3)
2. Python-OSC (1.8.3)

### How to use
1. Import 'ParameterMultiplier.unitypackage' to your Unity Project
2. Add 'ParameterMultiplier.prefab' to your Avatar Object
3. Write the parameters you need to synchronize in the form of "parameter name, type" and add the file to the Parameter List. (See Parameter_LIST_example.txt)

<img width="443" alt="스크린샷 2024-02-14 133701" src="https://github.com/ELKIES-VRC/ParameterMultiplier/assets/159980894/976a3fd6-2878-4f80-9d99-28974b1322b8">

4. Before access VRChat, Run PM_OSC_Server.py (You need Python Environment with Python-OSC installed)
   
* If you hear that your avatar looks strange to others, select Action Menu - Expressions - PM - ManualSync. Resynchronize all parameters.

### Limitations (Known Issues)
1. Resetting an avatar would cause the OSC server to die as all avatar-related saves inside the VRChat cache folder would be lost
2. Parameters are not automatically synchronized for people who come in after you've joined world instance
3. Parameters not syncing perfectly for everyone for unknown reasons in a crowded environment
4. The project is intended to target parameters that do not require real-time synchronization (e.g., closet). Please use Sync options for parameters that require real-time synchronization (e.g., facial tracking).


## License
Project Name : ParameterMultiplier

MIT License

Copyright (c) 2024 ELKIES-VRC

This software is distributed under the MIT License.

For more details, refer to the LICENSE file.

----
----

This project uses the following Open Source Softwares.

---

OpenSource Name : modular-avatar

Link : https://github.com/bdunderscore/modular-avatar

MIT License

Copyright (c) 2022 bd_

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

OpenSource Name : python-osc

Link : https://github.com/attwad/python-osc

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>

---
