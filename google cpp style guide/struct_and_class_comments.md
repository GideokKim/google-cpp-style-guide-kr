# 구조체와 클래스 주석 (Struct and Class Comments)

명확하지 않은 모든 클래스 또는 구조체 선언에는 해당 선언의 용도와 사용 방법을 설명하는 주석이 함께 있어야 합니다.

```cpp
// Iterates over the contents of a GargantuanTable.
// Example:
//    std::unique_ptr<GargantuanTableIterator> iter = table->NewIterator();
//    for (iter->Seek("foo"); !iter->done(); iter->Next()) {
//      process(iter->key(), iter->value());
//    }
class GargantuanTableIterator {
  ...
};
```

클래스 코멘트는 독자에게 클래스를 언제, 어떻게 사용해야 하는지 알 수 있는 충분한 정보와 클래스를 올바르게 사용하는 데 필요한 추가 고려 사항을 제공해야 합니다. 클래스가 설정한 동기화 가정이 있는 경우 이를 문서화하세요. 여러 스레드에서 클래스의 인스턴스에 액세스할 수 있는 경우 다중 스레드 사용과 관련된 규칙 및 불변성을 문서화하는 데 특히 주의하십시오.

클래스 주석은 클래스의 간단하고 집중적인 사용법을 보여주는 작은 예제 코드 조각을 위한 좋은 장소인 경우가 많습니다.

충분히 분리된 경우(예: .h 및 .cc 파일) 클래스 사용을 설명하는 주석은 해당 인터페이스 정의와 함께 표시되어야 합니다. 클래스 작업 및 구현에 대한 설명은 클래스 메서드 구현과 함께 제공되어야 합니다.

---

## 이해하기 쉽게 설명하기

### 핵심: 명확하지 않은 클래스·구조체에는 용도·사용법 주석을

자명하지 않은 모든 클래스/구조체 선언에는 **무엇을 위한 것이고 어떻게 쓰는지**를 설명하는 주석을 답니다. 짧은 사용 예제 코드를 함께 두면 좋습니다.

```cpp
// GargantuanTable의 내용을 순회한다.
// 예:
//    std::unique_ptr<GargantuanTableIterator> iter = table->NewIterator();
//    for (iter->Seek("foo"); !iter->done(); iter->Next()) {
//      process(iter->key(), iter->value());
//    }
class GargantuanTableIterator { ... };
```

### 무엇을 담나

- 언제·어떻게 써야 하는지, 올바르게 쓰기 위한 추가 고려사항.
- **동기화 가정**: 여러 스레드에서 접근될 수 있으면 멀티스레드 사용 규칙·불변식을 특히 주의해 문서화.

### 어디에 두나

- 클래스 **사용법** 주석 → 인터페이스 정의(`.h`) 옆.
- 클래스 **동작·구현** 설명 → 메서드 구현(`.cc`) 옆.
