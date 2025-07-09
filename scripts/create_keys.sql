-- productos → categorias
ALTER TABLE productos
ADD CONSTRAINT fk_productos_categoriaid
FOREIGN KEY (categoriaid)
REFERENCES categorias(categoriaid);

-- direccionesenvio → usuarios
ALTER TABLE direccionesenvio
ADD CONSTRAINT fk_direccionesenvio_usuarioid
FOREIGN KEY (usuarioid)
REFERENCES usuarios(usuarioid);

-- carrito → usuarios
ALTER TABLE carrito
ADD CONSTRAINT fk_carrito_usuarioid
FOREIGN KEY (usuarioid)
REFERENCES usuarios(usuarioid);

-- carrito → productos
ALTER TABLE carrito
ADD CONSTRAINT fk_carrito_productoid
FOREIGN KEY (productoid)
REFERENCES productos(productoid);

-- ordenes → usuarios
ALTER TABLE ordenes
ADD CONSTRAINT fk_ordenes_usuarioid
FOREIGN KEY (usuarioid)
REFERENCES usuarios(usuarioid);

-- ordenes → direccionesenvio
ALTER TABLE ordenes
ADD CONSTRAINT fk_ordenes_direccionid
FOREIGN KEY (direccionid)
REFERENCES direccionesenvio(direccionid);

-- detalleordenes → ordenes
ALTER TABLE detalleordenes
ADD CONSTRAINT fk_detalleordenes_ordenid
FOREIGN KEY (ordenid)
REFERENCES ordenes(ordenid);

-- detalleordenes → productos
ALTER TABLE detalleordenes
ADD CONSTRAINT fk_detalleordenes_productoid
FOREIGN KEY (productoid)
REFERENCES productos(productoid);

-- ordenesmetodospago → ordenes
ALTER TABLE ordenesmetodospago
ADD CONSTRAINT fk_ordenesmetodospago_ordenid
FOREIGN KEY (ordenid)
REFERENCES ordenes(ordenid);

-- ordenesmetodospago → metodospago
ALTER TABLE ordenesmetodospago
ADD CONSTRAINT fk_ordenesmetodospago_metodopagoid
FOREIGN KEY (metodopagoid)
REFERENCES metodospago(metodopagoid);

-- historialpagos → ordenes
ALTER TABLE historialpagos
ADD CONSTRAINT fk_historialpagos_ordenid
FOREIGN KEY (ordenid)
REFERENCES ordenes(ordenid);

-- historialpagos → metodospago
ALTER TABLE historialpagos
ADD CONSTRAINT fk_historialpagos_metodopagoid
FOREIGN KEY (metodopagoid)
REFERENCES metodospago(metodopagoid);

-- resenasproductos → usuarios
ALTER TABLE resenasproductos
ADD CONSTRAINT fk_resenasproductos_usuarioid
FOREIGN KEY (usuarioid)
REFERENCES usuarios(usuarioid);

-- resenasproductos → productos
ALTER TABLE resenasproductos
ADD CONSTRAINT fk_resenasproductos_productoid
FOREIGN KEY (productoid)
REFERENCES productos(productoid);
