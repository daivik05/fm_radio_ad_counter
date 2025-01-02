USE mp4;

CREATE TABLE mp4_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    extracted_date VARCHAR(10) NOT NULL  
);


USE mp4;
SELECT * FROM mp4_files;

ALTER TABLE mp4_files
ADD COLUMN ad_count INT NOT NULL DEFAULT 0;

