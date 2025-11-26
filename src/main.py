import os
from image_processor import get_contours
from curve_fitter import fit_curve_recursive
from pdf_generator import generate_pdf_from_curves

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
    output_filename = f"{name_without_ext}-output.pdf"
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"\nProcessing {input_path}...")
    
    try:
        # Get contours
        contours, (height, width, _) = get_contours(input_path)
        print(f"Found {len(contours)} contours.")
        
        all_curves = []
        total_curves_count = 0
        
        # Fit curves
        for i, contour in enumerate(contours):
            # print(f"Fitting contour {i+1}/{len(contours)} with {len(contour)} points...")
            curves = fit_curve_recursive(contour, error_threshold=2.0)
            all_curves.append(curves)
            total_curves_count += len(curves)
            
        print(f"Total Bézier curves generated: {total_curves_count}")
        
        # Generate PDF
        print(f"Generating PDF: {output_path}")
        generate_pdf_from_curves(all_curves, output_path, width, height)
        
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
