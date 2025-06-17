import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import jsPDF from 'jspdf';

@Component({
  selector: 'app-solve',
  templateUrl: './solve.component.html',
  styleUrls: ['./solve.component.scss']
})
export class SolveComponent {
  result: any;
  loading = false;
  isDarkMode = false;

  constructor(private http: HttpClient) {}

  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    this.loading = true;

    this.http.post<any>('http://localhost:8000/solve-doubt/', formData).subscribe({
      next: (data) => {
        this.result = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Upload error:', err);
        this.loading = false;
      }
    });
  }

  downloadAsPDF() {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text('🧠 AI Solved Doubt', 20, 20);
    doc.setFontSize(12);
    doc.text(`Question: ${this.result.question}`, 20, 40);
    doc.text(`Answer: ${this.result.answer}`, 20, 60);
    doc.save('doubt-answer.pdf');
  }
}
