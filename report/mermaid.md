# System Architecture & Flow Visualization

## 1. Module Structure (`src/fitting/`)

The curve fitting logic is modularized into the `src/fitting/` package to separate mathematical primitives from high-level strategies.

### A. `src/fitting/core.py` (Math Primitives)
Contains purely mathematical functions with no strategy logic.
*   **`chord_length_parameterize(points)`**: Assigns parameter values ($t$) to points based on chord length.
*   **`fit_cubic_bezier(points)`**: Solves the Least Squares system to fit a single cubic Bezier curve to a set of points.
*   **`calculate_max_error(points, curve)`**: Computes the maximum Euclidean distance between points and their corresponding curve positions.

### B. `src/fitting/pure.py` (Pure Interpolation Strategy)
*   **`fit_curve_pure_interpolation(points)`**: Connects every consecutive pair of points with a Bezier curve that behaves like a straight line. Used for high-fidelity but inefficient representation (1:1 compression).

### C. `src/fitting/recursive.py` (Hybrid/Recursive Strategy)
*   **`fit_curve_recursive(points, threshold)`**: A "Divide and Conquer" approach. Fits a curve, checks error; if error > threshold, splits the points at the max error index and recurses. Balances accuracy and curve count.

### D. `src/fitting/fixed.py` (Fixed Count Optimization)
*   **`fit_curves_to_fixed_count(contours, count)`**: Uses a Priority Queue (Heap) to iteratively split the curve segment with the highest error until a specific target curve count is reached.

---

## 2. Execution Flow Diagram

This diagram visualizes the data flow from user input in `main.py` through the selected strategy module.

```mermaid
graph TD
    %% Nodes
    Start((Start)) --> Input[main.py: User Input]
    Input --> Decision{Method?}
    
    %% Pure Branch
    Decision -->|Pure Interpolation| PureStart[Call src/fitting/pure.py]
    
    subgraph Pure_Module [src/fitting/pure.py]
        PureStart --> LoopPure[Iterate pairs]
        LoopPure --> CalcLinear[Calculate P1, P2 linearly]
        CalcLinear --> AddCurve[Add to List]
        AddCurve --> ReturnPure[Return Curves]
    end
    
    %% Hybrid Branch
    Decision -->|Hybrid/Recursive| HybridStart[Call src/fitting/recursive.py]
    
    subgraph Recursive_Module [src/fitting/recursive.py]
        HybridStart --> RecurseFit[fit_curve_recursive]
        
        subgraph Core_Module [src/fitting/core.py]
            RecurseFit --> FitCall[fit_cubic_bezier]
            FitCall --> Solve[Solve Least Squares]
            Solve --> ReturnCurve[Return Curve]
            
            ReturnCurve --> CalcErr[calculate_max_error]
        end
        
        CalcErr --> CheckErr{Error < Threshold?}
        
        CheckErr -->|Yes| Keep[Keep Curve]
        CheckErr -->|No| Split[Split & Recurse]
        Split --> RecurseFit
    end
    
    %% Fixed Branch
    Decision -->|Fixed Count| FixedStart[Call src/fitting/fixed.py]
    
    subgraph Fixed_Module [src/fitting/fixed.py]
        FixedStart --> InitHeap[Init Priority Queue]
        InitHeap --> PopWorst[Pop Worst Segment]
        PopWorst --> SplitFixed[Split & Re-fit]
        SplitFixed --> CheckCount{Count == Target?}
        CheckCount -->|No| PopWorst
        CheckCount -->|Yes| ReturnFixed[Return Curves]
    end
    
    %% Output
    ReturnPure --> PDF[pdf_generator.py]
    Keep --> PDF
    ReturnFixed --> PDF
    PDF --> End((End))
    
    %% Styling
    style Core_Module fill:#f9f,stroke:#333
    style Pure_Module fill:#e1f5fe,stroke:#01579b
    style Recursive_Module fill:#fff3e0,stroke:#ff6f00
    style Fixed_Module fill:#e8f5e9,stroke:#2e7d32
```
