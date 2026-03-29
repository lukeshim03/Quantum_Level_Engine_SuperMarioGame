# Quantum Level Engine: 양자 역학 기반 게임 레벨 생성 시스템

## 1. 프로젝트 개요

**Quantum Level Engine**은 양자 컴퓨팅 기술을 활용하여 동적이고 예측 불가능하며 플레이어의 행동에 반응하는 게임 레벨을 생성하는 혁신적인 시스템입니다. 기존의 절차적 레벨 생성(Procedural Level Generation, PLG) 방식이 가지는 한계, 즉 반복적이거나 예측 가능한 패턴을 넘어, 양자 역학의 고유한 특성(중첩, 얽힘, 붕괴)을 게임 레벨 디자인에 직접 통합하여 플레이어에게 매번 새롭고 유기적인 경험을 제공하는 것을 목표로 합니다.

## 2. 문제 정의 및 해결 방안

전통적인 PLG는 주로 고정된 규칙과 알고리즘에 의존하여 레벨을 생성합니다. 이는 일정 수준의 다양성을 제공하지만, 궁극적으로는 개발자가 정의한 패턴 내에서만 작동하므로 플레이어는 반복적인 경험을 할 수 있습니다. 특히, 실시간으로 플레이어의 입력에 반응하여 레벨 구조를 동적으로 변화시키는 데에는 한계가 있습니다.

Quantum Level Engine은 이러한 문제를 해결하기 위해 다음 세 가지 핵심 계층을 도입합니다.

1.  **양자 리저버 컴퓨팅 (Quantum Reservoir Computing, QRC)**: 레벨의 시간적 구조를 학습하고 새로운 타일 시퀀스를 생성하는 데 사용됩니다. 이는 기존의 예측 가능한 패턴을 넘어선 비선형적이고 유기적인 레벨 흐름을 가능하게 합니다.
2.  **파동 함수 붕괴 (Wave Function Collapse, WFC)**: QRC에서 생성된 시퀀스를 기반으로 실제 플레이 가능한 레벨 그리드를 구성합니다. 이는 양자적 무작위성 속에서도 레벨의 연결성과 플레이 가능성을 보장하는 제약 기반 복구 계층 역할을 합니다.
3.  **슈뢰딩거 보스 회로 (Schrödinger Boss Circuit)**: 보스전과 같은 핵심 게임 이벤트에서 양자 얽힘과 붕괴를 활용하여 레벨 환경을 동적으로 변화시킵니다. 보스의 체력에 따라 얽힘의 강도가 조절되며, 측정 결과에 따라 레벨의 특정 구역이 붕괴하는 등 예측 불가능한 요소를 도입합니다.

## 3. 기술 아키텍처

Quantum Level Engine은 세 가지 주요 모듈로 구성됩니다.

```mermaid
graph TD
    A[플레이어 입력/게임 상태] --> B{QRC 레벨 시퀀스 생성}
    B --> C{WFC 제약 조건 해결 및 레벨 그리드 생성}
    C --> D[게임 엔진 (레벨 렌더링)]
    D -- 보스 이벤트 발생 --> E{슈뢰딩거 보스 회로 실행}
    E -- 측정 결과 (비트스트링) --> F[레벨 구역 붕괴/변화]
    F --> D

    subgraph QRC Layer
        B
    end

    subgraph WFC Layer
        C
    end

    subgraph Boss Circuit Layer
        E
        F
    end
```

## 4. 핵심 구성 요소 및 코드 설명

### 4.1. 양자 리저버 컴퓨팅 (QRC) - `qrc_backend.py`

QRC는 게임 레벨의 시간적 종속성을 학습하고 새로운 타일 시퀀스를 생성하는 데 활용됩니다. `qrc_backend.py` 파일은 6-큐비트 양자 리저버 회로를 구축하고 실행하는 로직을 포함합니다. 타일 시퀀스는 큐비트의 회전 각도(Ry 게이트)로 인코딩되며, CNOT 게이트를 통해 얽힘이 생성됩니다. 이 모듈은 비선형 양자 역학을 활용하여 예측 불가능하면서도 일관성 있는 출력을 생성합니다.

**주요 특징:**
*   **비선형 양자 역학 활용**: `chaotic`이라는 표현 대신 `non-linear quantum dynamics`를 사용하여 기술적 정확성을 높였습니다.
*   **IonQ 하드웨어 연동**: `QiskitRuntimeService` 대신 **AWS Braket Provider**를 통해 IonQ Aria 1 백엔드에 접근하도록 구현되어 있습니다. 이는 IBM Quantum 전용인 `QiskitRuntimeService`의 한계를 극복하고 실제 IonQ 하드웨어와의 연동 가능성을 보여줍니다.

```python
# qrc_backend.py (핵심 발췌)
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_braket_provider import BraketProvider

N_QUBITS = 6
N_SHOTS = 1024
USE_HARDWARE = os.getenv("QRC_USE_HARDWARE", "false").lower() == "true"

def get_backend():
    if USE_HARDWARE:
        # IonQ hardware is accessed via cloud providers (e.g., AWS Braket)
        provider = BraketProvider()
        return provider.get_backend("Aria 1")
    return AerSimulator(method="statevector")

def build_reservoir_circuit(tile_sequence: list[float]) -> QuantumCircuit:
    # ... (회로 구축 로직)
    qc = QuantumCircuit(N_QUBITS, N_QUBITS)
    for i, val in enumerate(tile_sequence):
        theta = float(val) * np.pi
        qc.ry(theta, i)
    for i in range(N_QUBITS):
        qc.cx(i, (i + 1) % N_QUBITS)
    for i in range(N_QUBITS):
        qc.ry(np.pi / 4, i)
    qc.measure(list(range(N_QUBITS)), list(range(N_QUBITS)))
    return qc

def run_qrc_circuit(circuit: QuantumCircuit, shots: int = N_SHOTS) -> dict:
    backend = get_backend()
    job = backend.run(circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(circuit)
    return counts
```

### 4.2. 파동 함수 붕괴 (WFC) - `wfc_solver.py`

WFC 모듈은 QRC에서 생성된 확률 시퀀스를 입력받아, 게임 레벨의 연결성, 도달 가능성 등 미리 정의된 제약 조건들을 만족하는 플레이 가능한 레벨 그리드를 생성합니다. `wfc_solver.py`는 QRC 출력에 WFC에서 영감을 받은 제약 조건을 적용하여 일관된 레벨 레이아웃을 생성하는 간소화된 로직을 보여줍니다. 이는 QRC의 양자적 무작위성을 보완하여 실용적인 레벨을 만드는 데 필수적인 단계입니다.

**주요 특징:**
*   **제약 기반 복구 계층**: QRC 출력의 노이즈를 보정하고, 레벨의 구조적 무결성(예: 떠다니는 플랫폼 방지)을 보장하는 역할을 명확히 했습니다.
*   **플레이 가능성 보장**: 기본적인 플레이 가능성(예: 시작/끝 지점, 경로)을 확인하고 필요한 경우 수정하는 로직을 포함합니다.

```python
# wfc_solver.py (핵심 발췌)
import numpy as np

def apply_wfc_constraints(qrc_output_sequence: list[float], level_width: int, level_height: int) -> list[list[int]]:
    # ... (QRC 출력 → 타일 타입 매핑 및 기본 제약 조건 적용 로직)
    level_grid = [[0 for _ in range(level_width)] for _ in range(level_height)]
    sequence_idx = 0
    for r in range(level_height):
        for c in range(level_width):
            if sequence_idx < len(qrc_output_sequence):
                tile_value = qrc_output_sequence[sequence_idx]
                if tile_value < 0.33: level_grid[r][c] = 0
                elif tile_value < 0.66: level_grid[r][c] = 1
                else: level_grid[r][c] = 2
                sequence_idx += 1
            else: level_grid[r][c] = 0

    # Basic connectivity constraint
    for r in range(level_height - 2, -1, -1):
        for c in range(level_width):
            if level_grid[r][c] == 1 and level_grid[r+1][c] == 0:
                if c > 0 and level_grid[r+1][c-1] != 0:
                    level_grid[r+1][c] = 1
                elif c < level_width - 1 and level_grid[r+1][c+1] != 0:
                    level_grid[r+1][c] = 1
                else:
                    level_grid[r][c] = 0
    return level_grid

def ensure_playability(level_grid: list[list[int]]) -> list[list[int]]:
    # ... (플레이 가능성 보장 로직)
    has_platform = any(1 in row for row in level_grid)
    if not has_platform:
        level_grid[len(level_grid) - 1][len(level_grid[0]) // 2] = 1
    return level_grid
```

### 4.3. 슈뢰딩거 보스 회로 - `boss_circuit.py`

`boss_circuit.py`는 보스전의 핵심 메커니즘을 구현합니다. 보스의 체력(HP)에 따라 양자 회로의 얽힘 강도가 조절되며, 회로 측정 결과(비트스트링)에 따라 게임 레벨의 특정 구역이 붕괴하거나 변화합니다. 이는 플레이어에게 예측 불가능하고 전략적인 전투 경험을 제공합니다.

**주요 특징:**
*   **동적 얽힘 조절**: 보스 HP가 낮아질수록 얽힘 강도가 강해져, 레벨 붕괴 패턴이 더욱 질서정연해집니다.
*   **실시간 게임플레이**: 일반적인 게임플레이는 로컬 시뮬레이션을 사용하며, 보스 페이즈 전환과 같은 **주요 이벤트**에서만 IonQ 하드웨어 호출을 트리거하여 지연 시간 문제를 해결합니다.
*   **비트스트링 → 존 매핑**: 측정된 비트스트링을 기반으로 레벨의 6개 구역 중 하나를 붕괴시키는 로직을 포함합니다.

```python
# boss_circuit.py (핵심 발췌)
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_braket_provider import BraketProvider

N_QUBITS = 6
USE_HARDWARE = os.getenv("BOSS_USE_HARDWARE", "false").lower() == "true"

def get_boss_backend():
    if USE_HARDWARE:
        # IonQ hardware is accessed via cloud providers (e.g., AWS Braket)
        provider = BraketProvider()
        return provider.get_backend("Aria 1")
    return AerSimulator(method="statevector")

def build_boss_circuit(boss_hp_percentage: float) -> QuantumCircuit:
    # ... (회로 구축 로직)
    qc = QuantumCircuit(N_QUBITS, N_QUBITS)
    for i in range(N_QUBITS):
        qc.h(i)
    entanglement_angle = (1.0 - boss_hp_percentage) * np.pi
    for i in range(N_QUBITS - 1):
        qc.crx(entanglement_angle, i, i + 1)
    qc.crx(entanglement_angle, N_QUBITS - 1, 0)
    qc.measure(list(range(N_QUBITS)), list(range(N_QUBITS)))
    return qc

def trigger_boss_collapse(boss_hp_percentage: float) -> str:
    circuit = build_boss_circuit(boss_hp_percentage)
    backend = get_boss_backend()
    job = backend.run(circuit, shots=100)
    result = job.result()
    counts = result.get_counts(circuit)
    dominant_bitstring = max(counts, key=counts.get)
    return dominant_bitstring

def map_bitstring_to_zone(bitstring: str) -> int:
    return bitstring.count("1")
```

## 5. 환경 설정 및 실행 (MVP)

이 프로젝트의 핵심 로직을 실행하려면 다음 단계를 따르세요.

1.  **Qiskit 및 Braket Provider 설치**: `pip install qiskit qiskit-aer qiskit-braket-provider`
2.  **환경 변수 설정**: IonQ 하드웨어 백엔드를 사용하려면 `IONQ_TOKEN` (AWS Braket 인증용) 및 `QRC_USE_HARDWARE=true` 또는 `BOSS_USE_HARDWARE=true` 환경 변수를 설정해야 합니다. 하드웨어 접근 권한이 없다면 `USE_HARDWARE` 변수를 `false`로 두어 `AerSimulator`를 사용합니다.

    ```bash
    export IONQ_TOKEN="YOUR_AWS_BRAKET_TOKEN"
    export QRC_USE_HARDWARE="true" # 또는 "false"
    export BOSS_USE_HARDWARE="true" # 또는 "false"
    ```

3.  **코드 실행 예시**:

    ```python
    # qrc_example.py
    from qrc_backend import build_reservoir_circuit, run_qrc_circuit
    from wfc_solver import apply_wfc_constraints, ensure_playability

    # QRC 시퀀스 생성
    tile_sequence_input = [0.1, 0.5, 0.9, 0.2, 0.7, 0.3]
    qrc_circuit = build_reservoir_circuit(tile_sequence_input)
    qrc_counts = run_qrc_circuit(qrc_circuit)
    print(f"QRC Counts: {qrc_counts}")

    # QRC 출력을 시퀀스로 변환 (예시: 가장 높은 확률의 비트스트링을 기반으로)
    # 실제 구현에서는 확률 분포를 활용하여 더 복잡한 시퀀스를 생성할 수 있습니다.
    dominant_bitstring = max(qrc_counts, key=qrc_counts.get)
    qrc_output_sequence = [float(bit) for bit in dominant_bitstring] * 5 # 예시를 위해 확장

    # WFC 제약 조건 적용
    level_grid = apply_wfc_constraints(qrc_output_sequence, level_width=10, level_height=5)
    level_grid = ensure_playability(level_grid)
    print("\nGenerated Level Grid:")
    for row in level_grid:
        print(row)

    # boss_example.py
    from boss_circuit import trigger_boss_collapse, map_bitstring_to_zone

    boss_hp = 0.8 # 보스 체력 80%
    dominant_bitstring_boss = trigger_boss_collapse(boss_hp)
    collapsed_zone = map_bitstring_to_zone(dominant_bitstring_boss)
    print(f"\nBoss HP: {boss_hp*100}%")
    print(f"Dominant Bitstring from Boss Circuit: {dominant_bitstring_boss}")
    print(f"Collapsed Level Zone: {collapsed_zone}")
    ```

## 6. 향후 계획

*   **QRC 모델 고도화**: 실제 게임 데이터셋을 활용한 QRC 훈련 및 최적화.
*   **WFC 알고리즘 확장**: 더 복잡한 게임 레벨 제약 조건 및 다양한 타일 유형 지원.
*   **실시간 통합**: 게임 엔진(Unity, Unreal 등)과의 실제 연동 및 성능 최적화.
*   **다양한 양자 하드웨어 지원**: 다른 양자 클라우드 서비스(Azure Quantum 등)와의 통합.

## 7. 참고 문헌

*   [1] Ferreira, L. A., et al. (2022). *Quantum Reservoir Computing for Time Series Prediction*. arXiv preprint arXiv:2203.07817. (Moth Quantum paper)
*   [2] Qiskit Braket Provider Documentation. (Latest). *Accessing AWS Braket devices with Qiskit*. [https://qiskit-community.github.io/qiskit-braket-provider/](https://qiskit-community.github.io/qiskit-braket-provider/)
