library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
Library UNISIM;
use UNISIM.vcomponents.all;


entity DistilBERT is
    port (
        clk: in std_logic;
        resetn: in std_logic;
        resetp: in std_logic;
        start: in std_logic;
        enable: std_logic;
        done: out std_logic;
        rx: in std_logic;
        matrix1: in std_logic_vector(7 downto 0);
        matrix2: in std_logic_vector(7 downto 0);
        --input_data: in signed(31 downto 0);
        data_out: out std_logic
    );
end DistilBERT;


architecture behavioral of DistilBERT is



    component matrix_mult is
    port (
        clk: in std_logic;
        reset: in std_logic;
        input_ready: in std_logic;
        matrix1: in std_logic_vector(7 downto 0);
        matrix2: in std_logic_vector(7 downto 0);
        output_ready: out std_logic;
        result: out std_logic_vector(15 downto 0) -- Change this to 32 bits
    );
end component;

        component serializer is
    port (
        clk: in std_logic;
        reset: in std_logic;
        enable: in std_logic; 
        data_in: in signed(31 downto 0); -- modified to signed
        data_out: out std_logic
    );
end component;




    component relu is
        port (
            clk: in std_logic;
            reset: in std_logic;
            input_ready: in std_logic;
            input_val: in signed(31 downto 0);
            output_ready: out std_logic;
            output_val: out signed(31 downto 0)
        );
    end component;

    component softmax is
        port (
            clk: in std_logic;
            reset: in std_logic;
            input_ready: in std_logic;
            input_val: in signed(31 downto 0);
            output_ready: out std_logic;
            output_val: out signed(31 downto 0)
        );
    end component;

    component data_memory is
        port (
            clk: in std_logic;
            reset: in std_logic;
            wr_en: in std_logic;
            rd_en: in std_logic;
            addr: in unsigned(7 downto 0);
            wr_data: in signed(31 downto 0);
            rd_data: out signed(31 downto 0)
        );
    end component;

    component control is
        port (
            clk: in std_logic;
            reset: in std_logic;
            start: in std_logic;
            done: out std_logic
        );
    end component;
    
    component uart_receiver is
        generic (
            baud_rate: integer := 9600;
            clock_freq: integer := 50000000
        );
        port (
            clk: in std_logic;
            reset: in std_logic;
            rx: in std_logic;
            data_ready: out std_logic;
            data: out std_logic_vector(7 downto 0)
        );
    end component;

    -- intermediate signals
    signal reset: std_logic;
    signal mat_mult_result: std_logic_vector(31 downto 0); -- updated to 32-bit
    signal relu_result, softmax_result: signed(31 downto 0);
    signal memory_rd_data: signed(31 downto 0);
    signal uart_data_ready: std_logic;
    signal serialized_output: std_logic;
    signal uart_data: std_logic_vector(7 downto 0);

begin
    -- Instantiate and connect modules

       -- Serializer
            Serializer2: serializer
    port map (
        clk => clk,
        reset => reset,
        enable => enable,
        data_in => memory_rd_data, -- now memory_rd_data type matches data_in
        data_out => data_out
    );

    
    MatMul: matrix_mult
    port map (
        clk => clk,
        reset => reset,
        input_ready => start, -- You need to adjust this according to your control strategy
        matrix1 => matrix1,
        matrix2 => matrix2,
        output_ready => open, -- You need to handle this signal according to your control strategy
        result => mat_mult_result(15 downto 0) -- Only using 16 bits of the 32-bit 'mat_mult_result' signal
    );


    ActFunc: relu
    port map (
        clk => clk,
        reset => reset,
        input_ready => '1', -- You need to adjust this according to your control strategy
        input_val => signed(mat_mult_result), -- You need to adjust this according to your control strategy
        output_ready => open, -- You need to handle this signal according to your control strategy
        output_val => relu_result
    );

    Softmax_module: softmax
    port map (
        clk => clk,
        reset => reset,
        input_ready => '1', -- You need to adjust this according to your control strategy
        input_val => relu_result, -- You need to adjust this according to your control strategy
        output_ready => open, -- You need to handle this signal according to your control strategy
        output_val => softmax_result
    );

    DataMem: data_memory
    port map (
        clk => clk,
        reset => reset,
        wr_en => '0', -- You need to adjust this according to your control strategy
        rd_en => '1', -- You need to adjust this according to your control strategy
        addr => (others => '0'), -- You need to adjust this according to your control strategy
        wr_data => softmax_result, -- You need to adjust this according to your control strategy
        rd_data => memory_rd_data
    );

    Control_module: control
    port map (
        clk => clk,
        reset => reset,
        start => start,
        done => done
    );
    
    UartRx: uart_receiver
    generic map (
        baud_rate => 9600,
        clock_freq => 50000000
    )
    port map (
        clk => clk,
        reset => reset,
        rx => rx,
        data_ready => uart_data_ready,
        data => uart_data
    );
    
   IBUFDS_inst : IBUFDS
   port map (
      O => reset,   -- 1-bit output: Buffer output
      I => resetp,   -- 1-bit input: Diff_p buffer input (connect directly to top-level port)
      IB => resetn  -- 1-bit input: Diff_n buffer input (connect directly to top-level port)
   );
    
--        data_out <= serialized_output;

end behavioral;
