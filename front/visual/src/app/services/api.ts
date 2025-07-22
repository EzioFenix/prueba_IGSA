import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Registro {
  id: number;
  titulo: string;
  descripcion: string | null;
  estado: number;
  fechaCreacion: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:5000/victormiguelbarrerapena';

  constructor(private http: HttpClient) { }

  getAll(): Observable<Registro[]> {
    return this.http.get<Registro[]>(this.apiUrl);
  }

  create(registro: Omit<Registro, 'id' | 'fechaCreacion'>): Observable<any> {
    return this.http.post(this.apiUrl, registro);
  }

  update(id: number, registro: Omit<Registro, 'id' | 'fechaCreacion'>): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, registro);
  }

  delete(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}