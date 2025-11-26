class PDFGenerator:
    def __init__(self, filename, width, height):
        self.filename = filename
        self.width = width
        self.height = height
        self.objects = []
        self.content_stream = []
        
    def add_object(self, content):
        obj_id = len(self.objects) + 1
        self.objects.append(content)
        return obj_id
        
    def add_curve(self, p0, p1, p2, p3):
        # PDF coordinates usually start from bottom-left.
        # If our image coordinates are top-left, we might need to flip Y.
        # For now, we assume the points are already in the desired coordinate system
        # or we flip them here. Let's flip them here assuming input is image coords (y down).
        
        h = self.height
        
        # Move to P0
        self.content_stream.append(f"{p0.x:.2f} {h - p0.y:.2f} m")
        # Curve to P3 via P1, P2
        self.content_stream.append(f"{p1.x:.2f} {h - p1.y:.2f} {p2.x:.2f} {h - p2.y:.2f} {p3.x:.2f} {h - p3.y:.2f} c")
        
    def add_stroke(self):
        self.content_stream.append("S")
        
    def add_fill(self):
        self.content_stream.append("f")

    def generate(self):
        # 1. Header
        pdf_content = "%PDF-1.4\n"
        
        # 2. Objects
        offsets = []
        
        # Object 1: Catalog
        offsets.append(len(pdf_content))
        pdf_content += "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        
        # Object 2: Pages
        offsets.append(len(pdf_content))
        pdf_content += "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        
        # Object 3: Page
        offsets.append(len(pdf_content))
        pdf_content += f"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width} {self.height}] /Contents 4 0 R >>\nendobj\n"
        
        # Object 4: Content Stream
        stream_data = "\n".join(self.content_stream)
        stream_len = len(stream_data)
        
        offsets.append(len(pdf_content))
        pdf_content += f"4 0 obj\n<< /Length {stream_len} >>\nstream\n{stream_data}\nendstream\nendobj\n"
        
        # 3. Xref
        xref_start = len(pdf_content)
        pdf_content += "xref\n"
        pdf_content += f"0 {len(offsets) + 1}\n"
        pdf_content += "0000000000 65535 f \n"
        for offset in offsets:
            pdf_content += f"{offset:010d} 00000 n \n"
            
        # 4. Trailer
        pdf_content += "trailer\n"
        pdf_content += f"<< /Size {len(offsets) + 1} /Root 1 0 R >>\n"
        pdf_content += "startxref\n"
        pdf_content += f"{xref_start}\n"
        pdf_content += "%%EOF"
        
        with open(self.filename, 'w') as f:
            f.write(pdf_content)

def generate_pdf_from_curves(curves, output_filename, width, height):
    pdf = PDFGenerator(output_filename, width, height)
    
    # We can group curves that are connected, but for simplicity
    # we can just treat each curve as a sub-path.
    # Ideally, we should detect closed loops for filling.
    # The 'curves' input is a list of lists of curves (one list per contour).
    
    for contour_curves in curves:
        if not contour_curves:
            continue
            
        # Start path
        p0 = contour_curves[0][0]
        h = height
        pdf.content_stream.append(f"{p0.x:.2f} {h - p0.y:.2f} m")
        
        for curve in contour_curves:
            # curve is [p0, p1, p2, p3]
            # We assume p0 of this curve is p3 of previous, so we just issue 'c'
            p1, p2, p3 = curve[1], curve[2], curve[3]
            pdf.content_stream.append(f"{p1.x:.2f} {h - p1.y:.2f} {p2.x:.2f} {h - p2.y:.2f} {p3.x:.2f} {h - p3.y:.2f} c")
            
        # Close and stroke/fill
        # For now, let's just stroke.
        pdf.add_stroke()
        
    pdf.generate()
