"""
PDF report generation for motor diagnosis
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from pathlib import Path
from datetime import datetime
import json


class ReportGenerator:
    """Generate PDF diagnostic reports"""
    
    def __init__(self):
        self.report_dir = Path("reports")
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom styles for report"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.darkblue,
            spaceAfter=30
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.darkblue,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            spaceAfter=12
        ))
    
    def generate(self, motor_id: str, motor_type: str, rpm: float, load: float,
                 temperature: float, input_type: str, image_path: str, video_path: str,
                 text_input: str, predicted_fault: str, confidence: float,
                 severity: str, severity_score: float, probability_distribution: dict,
                 important_features: list, heatmap_path: str) -> str:
        """
        Generate PDF diagnostic report
        
        Returns:
            Path to generated report
        """
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"diagnosis_report_{timestamp}.pdf"
        report_path = self.report_dir / report_filename
        
        # Create PDF document
        doc = SimpleDocTemplate(str(report_path), pagesize=A4)
        story = []
        
        # Title
        title = Paragraph("Motor Vibration Fault Diagnosis Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Motor Information Section
        story.append(Paragraph("Motor Information", self.styles['CustomHeading']))
        
        motor_data = [
            ["Motor ID:", motor_id or "N/A"],
            ["Motor Type:", motor_type or "N/A"],
            ["RPM:", f"{rpm:.1f}" if rpm else "N/A"],
            ["Load:", f"{load:.1f}%" if load else "N/A"],
            ["Temperature:", f"{temperature:.1f}°C" if temperature else "N/A"],
            ["Date/Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        ]
        
        motor_table = Table(motor_data, colWidths=[1.5*inch, 3*inch])
        motor_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(motor_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Input Information Section
        story.append(Paragraph("Input Information", self.styles['CustomHeading']))
        
        input_data = [
            ["Input Type:", input_type],
            ["Image:", image_path.split("\\")[-1] if image_path else "N/A"],
            ["Video:", video_path.split("\\")[-1] if video_path else "N/A"],
            ["Text Input:", text_input[:100] + "..." if text_input and len(text_input) > 100 else text_input or "N/A"]
        ]
        
        input_table = Table(input_data, colWidths=[1.5*inch, 3*inch])
        input_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(input_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Diagnosis Results Section
        story.append(Paragraph("Diagnosis Results", self.styles['CustomHeading']))
        
        # Highlight predicted fault
        fault_color = colors.red if severity == "High" else colors.orange if severity == "Medium" else colors.green
        
        diagnosis_data = [
            ["Predicted Fault:", predicted_fault],
            ["Confidence:", f"{confidence:.2%}"],
            ["Severity:", severity],
            ["Severity Score:", f"{severity_score:.1f}/100"]
        ]
        
        diagnosis_table = Table(diagnosis_data, colWidths=[1.5*inch, 3*inch])
        diagnosis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (1, 0), (1, 0), fault_color),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(diagnosis_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Probability Distribution
        story.append(Paragraph("Probability Distribution", self.styles['CustomHeading']))
        
        prob_data = [["Fault Class", "Probability"]]
        for fault, prob in probability_distribution.items():
            prob_data.append([fault, f"{prob:.2%}"])
        
        prob_table = Table(prob_data, colWidths=[2*inch, 2.5*inch])
        prob_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(prob_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Important Features
        story.append(Paragraph("Important Features", self.styles['CustomHeading']))
        
        feature_data = [["Feature", "Contribution", "Value"]]
        for feature in important_features:
            feature_data.append([
                feature.get("feature", "N/A"),
                feature.get("contribution", "N/A"),
                feature.get("value", "N/A")
            ])
        
        feature_table = Table(feature_data, colWidths=[2*inch, 1.5*inch, 1*inch])
        feature_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(feature_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        story.append(Paragraph("Recommendations", self.styles['CustomHeading']))
        
        recommendation = self._get_recommendation(predicted_fault, severity)
        rec_paragraph = Paragraph(recommendation, self.styles['CustomBody'])
        story.append(rec_paragraph)
        story.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        story.append(Paragraph("Disclaimer", self.styles['CustomHeading']))
        
        disclaimer = (
            "This system provides model-based diagnostic assistance based on visual pattern analysis. "
            "Final maintenance decisions should be confirmed using appropriate electrical, mechanical, "
            "and vibration measurements by qualified personnel. The predictions are based on pattern "
            "recognition and should be used as supplementary information for diagnosis."
        )
        
        disclaimer_paragraph = Paragraph(disclaimer, self.styles['CustomBody'])
        story.append(disclaimer_paragraph)
        
        # Build PDF
        doc.build(story)
        
        return str(report_path)
    
    def _get_recommendation(self, fault: str, severity: str) -> str:
        """Get recommendation based on fault and severity"""
        recommendations = {
            "Healthy": "Motor appears to be operating normally. Continue regular maintenance schedule.",
            "Rotor Unbalance": "Inspect rotor for mass distribution issues. Consider dynamic balancing if vibration levels exceed acceptable limits.",
            "Shaft Misalignment": "Check shaft alignment using laser alignment tools. Adjust coupling as needed.",
            "Bearing Fault": "Inspect bearings for wear, damage, or lubrication issues. Consider bearing replacement if necessary.",
            "Rotor Fault": "Inspect rotor for broken bars, asymmetry, or mechanical defects. Perform electrical tests if applicable.",
            "Stator Fault": "Check stator windings for abnormalities, inter-turn faults, or electrical asymmetry. Perform insulation resistance testing.",
            "Mechanical Looseness": "Inspect mounting bolts, foundation, and structural connections. Tighten or replace as needed.",
            "Coupling Fault": "Inspect coupling for wear, misalignment, or mechanical damage. Replace if necessary."
        }
        
        base_recommendation = recommendations.get(fault, "Consult maintenance manual for specific fault diagnosis procedures.")
        
        if severity == "High":
            base_recommendation += " IMMEDIATE ACTION RECOMMENDED due to high severity."
        elif severity == "Medium":
            base_recommendation += " Schedule inspection at next available maintenance window."
        
        return base_recommendation
