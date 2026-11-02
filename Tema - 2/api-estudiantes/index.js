
const express = require("express");
const prisma = require("./prisma");

const app = express();
const PORT = 3000;

app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    mensaje: "API de estudiantes funcionando"
  });
});

app.get("/estudiantes", async (req, res) => {
  try {
    const estudiantes = await prisma.estudiante.findMany();

    res.status(200).json(estudiantes);
  } catch (error) {
    console.error("Error de Prisma:", error);

    res.status(500).json({
      error: "No se pudieron consultar los estudiantes"
    });
  }
});

app.post("/estudiantes", async (req, res) => {
  try {
    const { matricula, nombre, apellidos, carrera, correo } = req.body ?? {};

    if (
      ![matricula, nombre, apellidos, carrera, correo]
        .every(valor => typeof valor === "string" && valor.trim() !== "")
    ) {
      return res.status(400).json({
        error: "Todos los campos son obligatorios"
      });
    }

    const nuevoEstudiante = await prisma.estudiante.create({
      data: {
        matricula: matricula.trim(),
        nombre: nombre.trim(),
        apellidos: apellidos.trim(),
        carrera: carrera.trim(),
        correo: correo.trim()
      }
    });

    res.status(201).json({
      mensaje: "Estudiante registrado correctamente",
      estudiante: nuevoEstudiante
    });

  } catch (error) {
    console.error(error);

    if (error.code === "P2002") {
      return res.status(409).json({
        error: "La matrícula o el correo ya están registrados"
      });
    }

    res.status(500).json({
      error: "No se pudo registrar el estudiante"
    });
  }
});



app.put("/estudiantes/:id", async (req, res) => {
  try {
    const id = Number(req.params.id);

    if (!Number.isSafeInteger(id) || id <= 0) {
      return res.status(400).json({
        error: "El ID debe ser un número entero válido"
      });
    }

    const { matricula, nombre, apellidos, carrera, correo } = req.body ?? {};

    const datos = { matricula, nombre, apellidos, carrera, correo };

    if (
      Object.values(datos).some(
        valor => typeof valor !== "string" || valor.trim() === ""
      )
    ) {
      return res.status(400).json({
        error: "Los campos enviados deben contener texto válido"
      });
    }

    const campos = Object.fromEntries(
      Object.entries(datos)
        .filter(([, valor]) => valor !== undefined)
        .map(([clave, valor]) => [clave, valor.trim()])
    );

    if (Object.keys(campos).length === 0) {
      return res.status(400).json({
        error: "Debes enviar al menos un campo para actualizar"
      });
    }

    const estudiante = await prisma.estudiante.update({
      where: { id },
      data: campos
    });

    res.status(200).json({
      mensaje: "Estudiante actualizado correctamente",
      estudiante
    });

  } catch (error) {
    console.error(error);

    if (error.code === "P2025") {
      return res.status(404).json({
        error: "Estudiante no encontrado"
      });
    }

    if (error.code === "P2002") {
      return res.status(409).json({
        error: "La matrícula o el correo ya están registrados"
      });
    }

    res.status(500).json({
      error: "Error al actualizar estudiante"
    });
  }
});




app.delete("/estudiantes/:id", async (req, res) => {
  try {
    const id = Number(req.params.id);

    if (!Number.isSafeInteger(id) || id <= 0) {
      return res.status(400).json({
        error: "El ID debe ser un número entero válido"
      });
    }

    const estudiante = await prisma.estudiante.delete({
      where: { id }
    });

    res.status(200).json({
      mensaje: "Estudiante eliminado correctamente",
      estudiante
    });

  } catch (error) {
    console.error(error);

    if (error.code === "P2025") {
      return res.status(404).json({
        error: "Estudiante no encontrado"
      });
    }

    res.status(500).json({
      error: "Error al eliminar estudiante"
    });
  }
});


app.listen(PORT, () => {
  console.log(`Servidor ejecutándose en http://localhost:${PORT}`);
});



