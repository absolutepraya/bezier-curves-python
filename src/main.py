import os
from image_processor import get_contours
from curve_fitter import fit_curve_recursive
from png_generator import generate_png_from_curves

def main():
    input_dir = "input"
    output_dir = "output"
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 1. List images in input directory
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' not found.")
        return

    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    if not files:
        print(f"No image files found in '{input_dir}'.")
        return
        
    print("Available images:")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
        
    # 2. User selection
    while True:
        try:
            choice = input("\nSelect an image number to process: ")
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                filename = files[idx]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")
            
    input_path = os.path.join(input_dir, filename)
    
    # 3. Construct output filename
    name_without_ext = os.path.splitext(filename)[0]
    
    print(f"\nProcessing {input_path}...")
    
    try:
        # Get contours
        contours, (height, width, _) = get_contours(input_path)
        
        all_curves = []
        total_curves_count = 0
        total_points_count = 0
        
        # Fit curves
        for i, contour in enumerate(contours):
            total_points_count += len(contour)
            curves = fit_curve_recursive(contour, error_threshold=2.0)
            all_curves.append(curves)
            total_curves_count += len(curves)
            
        # Data Logging
        print("-" * 40)
        print(f"DATA LOGGING SUMMARY")
        print("-" * 40)
        print(f"Image Dimensions        : {width}x{height}")
        print(f"Total Contours Found    : {len(contours)}")
        print(f"Total Original Points   : {total_points_count}")
        print(f"Total Bezier Curves     : {total_curves_count}")
        if total_curves_count > 0:
            ratio = total_points_count / total_curves_count
            print(f"Compression Ratio       : 1 curve per {ratio:.2f} points")
        print("-" * 40)
        
        # Generate PNG
        png_output_filename = f"{name_without_ext}-output.png"
        png_output_path = os.path.join(output_dir, png_output_filename)
        print(f"Generating PNG: {png_output_path}")
        generate_png_from_curves(all_curves, png_output_path, width, height)
        
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
