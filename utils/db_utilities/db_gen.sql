/*****************************************************************
*                                                                *
* Create RAW test data Table                                     *
*                                                                * 
*****************************************************************/

DROP TABLE IF EXISTS raw_iv_data CASCADE;

CREATE TABLE raw_iv_data
(
    id SERIAL NOT NULL, 
    
    -- Device/Wafer info
    device_num TEXT NOT NULL,
    wafer_info TEXT NOT NULL,
    device_width INTEGER NOT NULL,
    device_length INTEGER NOT NULL,

    -- Test session info    
    dose TEXT NOT NULL,
    test_datetime TIMESTAMP NOT NULL,

    -- Test result
    gate_voltage FLOAT NOT NULL, --VG
    gate_current FLOAT NOT NULL, --IG
    drain_voltage FLOAT NOT NULL, --VD
    drain_current FLOAT NOT NULL, --ID
    body_current FLOAT NOT NULL, --IB
    source_current FLOAT NOT NULL, --IS 

    -- Test session data
    primary_contact TEXT NOT NULL DEFAULT 'HaoQiu_DEV',
    alternate_contact TEXT,

    -- DB timestamp for ref
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp,

    -- soft delelte
    deleted_at TIMESTAMP,

    CONSTRAINT raw_iv_pkey PRIMARY KEY(id)
);

CREATE INDEX raw_iv_index 
    ON raw_iv_data (device_num ASC, dose ASC, wafer_info ASC, test_datetime ASC) 
    WHERE deleted_at IS NULL;


/*****************************************************************
*                                                                *
* Create IV table                                                *
*                                                                * 
*****************************************************************/

DROP TABLE IF EXISTS analyzed_iv_data CASCADE;

CREATE TABLE analyzed_iv_data
(
    id SERIAL NOT NULL, 
    
    -- Device/Wafer info
    device_num TEXT NOT NULL,
    wafer_info TEXT NOT NULL,

    -- Test data    
    dose TEXT NOT NULL,
    device_width INTEGER NOT NULL,
    device_length INTEGER NOT NULL,

    -- Analyze result
    threshold_voltage_shift TEXT,
    on_current TEXT NOT NULL DEFAULT '99999999',
    off_current TEXT NOT NULL DEFAULT '99999999',
    threshold_voltage TEXT NOT NULL DEFAULT '99999999',

    -- Test session data
    analyzed_datetime TIMESTAMP NOT NULL,
    primary_contact TEXT NOT NULL DEFAULT 'HaoQiu_DEV',
    alternate_contact TEXT,

    -- DB timestamp for ref
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp,

    --soft delelte
    deleted_at TIMESTAMP,

    CONSTRAINT analyzed_iv_data_pkey PRIMARY KEY (wafer_info, device_num, dose)
);

CREATE UNIQUE INDEX analyzed_iv_data_index
    ON analyzed_iv_data (device_num ASC, dose ASC, wafer_info ASC) 
    WHERE deleted_at IS NULL;



/*****************************************************************
*                                                                *
* Create Triggers                                                *
*                                                                * 
*****************************************************************/

-- Update-time update Function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger (update raw_iv_data)
DROP TRIGGER IF EXISTS tg_raw_iv_data_updated_at ON public.raw_iv_data;
CREATE TRIGGER tg_raw_iv_data_updated_at
BEFORE UPDATE
ON raw_iv_data
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- Trigger (update iv_result)
DROP TRIGGER IF EXISTS tg_analyzed_iv_data_updated_at ON public.analyzed_iv_data;
CREATE TRIGGER tg_analyzed_iv_data_updated_at
BEFORE UPDATE
ON analyzed_iv_data
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();