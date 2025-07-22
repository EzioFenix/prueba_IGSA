// src/app/tabla/tabla.component.ts

// ===== PASO 1: Importar ChangeDetectorRef =====
import { Component, OnInit, ChangeDetectorRef } from '@angular/core'; 
import { ApiService, Registro } from '../services/api';
import { catchError, of } from 'rxjs';

// --- Imports necesarios ---
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// --- Imports de Angular Material ---
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'app-tabla',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule
  ],
  templateUrl: './tabla.html',
  styleUrls: ['./tabla.css']
})
export class TablaComponent implements OnInit {
  
  displayedColumns: string[] = ['titulo', 'descripcion', 'estado', 'acciones'];
  dataSource = new MatTableDataSource<Registro>([]);
  nuevoRegistro: { titulo: string; descripcion: string; estado: number | null } = { titulo: '', descripcion: '', estado: null };
  editandoId: number | null = null;
  mostrandoFormulario = false;

  estadosMapa = new Map<number, string>([
    [1, 'Pendiente'],
    [2, 'En Progreso'],
    [3, 'Completado']
  ]);

  // ===== PASO 2: Inyectar ChangeDetectorRef en el constructor =====
  constructor(
    private apiService: ApiService, 
    private cd: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.cargarRegistros();
  }

  cargarRegistros(): void {
    this.apiService.getAll().pipe(
      catchError(err => {
        alert('Error al cargar los datos: ' + err.message);
        return of([]);
      })
    ).subscribe(data => {
      this.dataSource.data = data;
    });
  }

  obtenerTextoEstado(estadoNumero: number): string {
    return this.estadosMapa.get(estadoNumero) || 'Desconocido';
  }

  agregar(): void {
    this.mostrandoFormulario = true;
    this.editandoId = null;
    this.nuevoRegistro = { titulo: '', descripcion: '', estado: null };
  }

  guardar(): void {
    if (!this.nuevoRegistro.titulo.trim() || this.nuevoRegistro.estado === null) {
      alert('El campo Título y Estado son obligatorios.');
      return;
    }

    const payload = {
      titulo: this.nuevoRegistro.titulo,
      descripcion: this.nuevoRegistro.descripcion,
      estado: this.nuevoRegistro.estado
    };
    
    const esEdicion = this.editandoId !== null;

    const operacion$ = esEdicion
      ? this.apiService.update(this.editandoId!, payload)
      : this.apiService.create(payload);

    operacion$.subscribe({
      next: () => {
        const mensajeExito = esEdicion ? 'Registro actualizado exitosamente.' : 'Registro creado exitosamente.';
        alert(mensajeExito);
        
        this.cargarRegistros();
        this.cancelar();
      },
      error: (err) => {
        const mensajeError = err.error?.error || err.error?.message || err.message;
        alert(`Error al ${esEdicion ? 'actualizar' : 'crear'}: ` + mensajeError);
      }
    });
  }

  editar(registro: Registro): void {
    this.editandoId = registro.id;
    this.nuevoRegistro = { 
      titulo: registro.titulo,
      descripcion: registro.descripcion || '', 
      estado: Number(registro.estado) 
    };
    this.mostrandoFormulario = true;
  }

  eliminar(id: number): void {
    if (confirm('¿Seguro que deseas eliminar este registro?')) {
      this.apiService.delete(id).subscribe({
        next: () => {
          const datosActuales = this.dataSource.data;
          this.dataSource.data = datosActuales.filter((registro: Registro) => registro.id !== id);
          alert('Registro eliminado correctamente.');
        },
        error: (err) => alert('Error al eliminar: ' + (err.error?.error || err.message))
      });
    }
  }

  cancelar(): void {
    this.mostrandoFormulario = false;
    this.editandoId = null;
    this.nuevoRegistro = { titulo: '', descripcion: '', estado: null };
    
    // ===== PASO 3: Forzar la detección de cambios =====
    // Esta línea le ordena a Angular que actualice la vista inmediatamente.
    this.cd.detectChanges();
  }
}