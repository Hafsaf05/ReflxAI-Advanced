# 🚀 ReflxAI-Advanced — Usage Examples

This guide shows you how to use the 6-agent system effectively.

---

## Example 1: Quick Code Generation

### Prompt
```
Write a Python function `is_palindrome(s: str) -> bool` that checks 
if a string is a palindrome, ignoring spaces and punctuation. 
Include type hints and docstring.
```

### What Happens

1. **Generator Agent** writes:
```python
def is_palindrome(s: str) -> bool:
    """Check if string is palindrome, ignoring spaces/punctuation."""
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```

2. **Critic Agent** reviews → `APPROVED`

3. **Test Agent** generates:
```python
def test_is_palindrome():
    assert is_palindrome("A man, a plan, a canal: Panama") == True
    assert is_palindrome("hello") == False
    assert is_palindrome("") == True
```

4. **Performance Agent** analyzes → `OPTIMIZED` (O(n) time, O(n) space)

5. **Security Agent** audits → `SECURE` (no vulnerabilities)

6. **Documentation Agent** enriches with full docstrings

7. **Metrics Dashboard** shows:
   - Overall Score: **92/100**
   - Test Coverage: **85%**
   - Security Score: **100/100**
   - Performance Score: **95/100**

---

## Example 2: Algorithm Challenge with Optimization

### Prompt
```
Implement a function `longest_substring_without_repeating(s: str) -> int` 
that finds the length of the longest substring without repeating characters 
using a sliding window approach.
```

### Pipeline Execution

**Generator (Iteration 1):**
```python
def longest_substring_without_repeating(s: str) -> int:
    char_index = {}
    max_length = 0
    start = 0
    for i, char in enumerate(s):
        if char in char_index:
            start = max(start, char_index[char] + 1)
        char_index[char] = i
        max_length = max(max_length, i - start + 1)
    return max_length
```

**Critic Feedback:**
- ✅ Algorithm is correct
- ✅ Time complexity O(n) is optimal
- ⚠️ Missing edge case handling for None/empty string

**Generator (Iteration 2):**
```python
def longest_substring_without_repeating(s: str) -> int:
    """Find length of longest substring without repeating characters.
    
    Args:
        s: Input string (can be None or empty).
        
    Returns:
        Length of longest substring without repeating chars.
        
    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    if not s:
        return 0
    
    char_index = {}
    max_length = 0
    start = 0
    
    for i, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        char_index[char] = i
        max_length = max(max_length, i - start + 1)
    
    return max_length
```

**Critic:** `APPROVED`

**Test Agent** generates 12 test cases covering:
- Empty string, single char, repeated chars
- Edge cases (None validation, etc.)
- Performance benchmarks

**Performance Agent:**
```
1. Current complexity: O(n) time, O(min(n, charset_size)) space ✅
2. Already using optimal sliding window approach ✅
3. Space could be reduced by using fixed-size array for ASCII (optimization #1)
```

**Security Agent:** `SECURE`

**Documentation Agent:** Adds comprehensive docstrings

**Metrics:**
```
Overall Score: 94/100
├─ Test Coverage: 90%
├─ Security: 100/100
├─ Performance: 92/100
└─ Complexity: 8/10
```

---

## Example 3: Data Structure Implementation

### Prompt
```
Implement an LRU Cache class with O(1) get and put operations. 
Use OrderedDict. Include comprehensive tests and docstrings.
```

### Result

**Generated Code:**
```python
from collections import OrderedDict
from typing import Optional, Any

class LRUCache:
    """Least Recently Used (LRU) Cache with O(1) operations.
    
    Uses OrderedDict to maintain insertion order and enable O(1) eviction.
    """
    
    def __init__(self, capacity: int):
        """Initialize LRU Cache.
        
        Args:
            capacity: Maximum number of items to store.
            
        Raises:
            ValueError: If capacity < 1.
        """
        if capacity < 1:
            raise ValueError("Capacity must be >= 1")
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: Any) -> Optional[Any]:
        """Get value by key, O(1) operation.
        
        Args:
            key: The key to look up.
            
        Returns:
            Value if key exists, None otherwise.
        """
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: Any, value: Any) -> None:
        """Put key-value pair, O(1) operation.
        
        If key exists, update and mark as recent.
        If cache is full, evict oldest (least recently used) item.
        
        Args:
            key: The key to set.
            value: The value to store.
        """
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

**Tests Generated:** 25 test cases
- Basic get/put operations
- Eviction order verification
- Edge cases (negative capacity, null values)
- Performance benchmarks

**Metrics:**
```
Overall Score: 96/100
├─ Test Coverage: 95%
├─ Security: 100/100
├─ Performance: 100/100 (O(1) confirmed)
└─ Complexity: 9/10 (excellent design)
```

---

## Example 4: Rapid Prototyping Mode

### Configuration (Sidebar)
```
Max Iterations: 1
Skip Agents: [Test, Performance, Security]
```

### Benefit
Generate code fast without waiting for all agents. Takes ~15 seconds instead of 3 minutes.

### Use Case
- **Rapid prototyping**
- **Interview prep** (quick solution generation)
- **Proof of concepts**

---

## Example 5: Security-Focused Code Review

### Prompt
```
Write a function to authenticate users with JWT tokens. 
Include validation, error handling, and expiration checks.
```

### Security Agent Output

```
FINDINGS: 3 Issues Detected

1. [HIGH] Weak secret key usage
   Location: Line 8 - secret = 'default_key'
   Fix: Use environment variables for secrets
   
2. [MEDIUM] Missing token expiration validation
   Location: Line 15 - jwt.decode(token, secret)
   Fix: Add 'exp' claim validation
   
3. [LOW] Verbose error messages
   Location: Line 20 - except jwt.InvalidTokenError as e
   Fix: Use generic error messages to avoid leaking info
```

### Metrics
```
Security Score: 45/100 ⚠️ (3 issues found)
Performance Score: 92/100
Test Coverage: 80%
Overall Score: 64/100 (below threshold)
```

### Next Step
Generator refactors based on Security feedback, and Security Agent re-audits.

---

## 🎯 Tips for Best Results

### For Algorithm Problems
1. Set Max Iterations: **3**
2. Enable Agents: **Test + Performance**
3. Focus on: Correctness, then optimization

### For Production Code
1. Set Max Iterations: **5**
2. Enable Agents: **All 6**
3. Review Security tab first

### For Rapid Prototyping
1. Set Max Iterations: **1**
2. Skip Agents: **Test, Performance, Docs**
3. Fast feedback in ~30 seconds

### For API Development
1. Set Max Iterations: **3**
2. Focus on: Security + Documentation agents
3. Review Security and Docs tabs

---

## 📥 Export Examples

### Option 1: Just Download Code
```
solution_output.py — Final code only
```

### Option 2: Code + Tests
```
solution_output.py
test_solution.py
```

### Option 3: Full Report
```
report_2024_06_09_150000.json
{
  "timestamp": "2024-06-09T15:00:00",
  "code": "...",
  "agent_outputs": {
    "critic": "APPROVED",
    "tests": "...",
    "performance": "OPTIMIZED",
    "security": "SECURE",
    "documented_code": "...",
    "quality_metrics": {
      "overall_score": 94.5,
      "test_coverage": 90,
      "security_score": 100,
      ...
    }
  }
}
```

---

## ⚡ Performance Tips

| Goal | Config |
|---|---|
| **Fast Prototype** | Max 1 iter, Skip all optional agents |
| **Quality Code** | Max 3 iter, Enable all agents |
| **Production Ready** | Max 5 iter, Enable all agents, Multiple reviews |
| **Interview Prep** | Max 2 iter, Enable tests + perf |

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|---|---|
| "Test coverage is 0%" | Check if test generation was skipped in config |
| "Performance score is low" | Review Performance tab recommendations |
| "Security vulnerabilities found" | Read Security tab details and request refactor |
| "Agents are slow" | Reduce max iterations or skip optional agents |

---

Made with ❤️ by the ReflxAI-Advanced team
